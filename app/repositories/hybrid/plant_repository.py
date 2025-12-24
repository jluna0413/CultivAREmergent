from typing import List, Optional, Any, Dict
import asyncio
import logging
from app.repositories.interfaces import PlantRepository, PlantDTO, ActivityDTO, PlantCreateDTO, PlantUpdateDTO
from app.repositories.sql.plant_repository import SQLPlantRepository
from app.repositories.algorand.plant_repository import AlgorandPlantRepository

logger = logging.getLogger(__name__)

class HybridPlantRepository(PlantRepository):
    """
    Orchestrates data access between SQL and Algorand repositories.
    Enables zero-downtime migration via dual-write pattern.
    """
    
    def __init__(
        self,
        sql_repo: SQLPlantRepository,
        algo_repo: AlgorandPlantRepository,
        migration_mode: str = "sql_only"  # sql_only, dual_write, blockchain_only
    ):
        self.sql = sql_repo
        self.algo = algo_repo
        self.mode = migration_mode

    async def create(self, plant_data: PlantCreateDTO) -> PlantDTO:
        if self.mode == "blockchain_only":
            return await self.algo.create(plant_data)
        
        # Primary write to SQL
        sql_result = await self.sql.create(plant_data)
        
        if self.mode == "dual_write":
            # Fire and forget blockchain write
            # We use the SQL ID to link them if possible, or mapping
            # For now, we just mirror the data creation
            asyncio.create_task(self._safe_algo_create(plant_data))
            
        return sql_result

    async def _safe_algo_create(self, data: PlantCreateDTO):
        try:
            await self.algo.create(data)
        except Exception as e:
            logger.error(f"HybridRepo: Failed to dual-write create to Algorand: {e}")

    async def get_by_id(self, plant_id: int | str) -> Optional[PlantDTO]:
        if self.mode == "blockchain_only":
            return await self.algo.get_by_id(plant_id)
        
        # Read from SQL (Fast)
        return await self.sql.get_by_id(int(plant_id))

    async def get_by_user(self, user_id: int) -> List[PlantDTO]:
        if self.mode == "blockchain_only":
            return await self.algo.get_by_user(user_id)
        
        return await self.sql.get_by_user(user_id)

    async def update(self, plant_id: int | str, plant_data: PlantUpdateDTO) -> PlantDTO:
        if self.mode == "blockchain_only":
            return await self.algo.update(plant_id, plant_data)
        
        sql_result = await self.sql.update(int(plant_id), plant_data)
        
        if self.mode == "dual_write":
            asyncio.create_task(self._safe_algo_update(plant_id, plant_data))
            
        return sql_result

    async def _safe_algo_update(self, plant_id, data):
        try:
            await self.algo.update(plant_id, data)
        except Exception as e:
            logger.error(f"HybridRepo: Failed to dual-write update to Algorand: {e}")

    async def delete(self, plant_id: int | str) -> bool:
        if self.mode == "blockchain_only":
            return await self.algo.delete(plant_id)
        
        sql_result = await self.sql.delete(int(plant_id))
        
        if self.mode == "dual_write":
            asyncio.create_task(self._safe_algo_delete(plant_id))
            
        return sql_result

    async def _safe_algo_delete(self, plant_id):
        try:
            await self.algo.delete(plant_id)
        except Exception as e:
            logger.error(f"HybridRepo: Failed to dual-write delete to Algorand: {e}")

    async def record_activity(
        self,
        plant_id: int | str,
        activity_type: str,
        details: Dict[str, Any]
    ) -> ActivityDTO:
        if self.mode == "blockchain_only":
            return await self.algo.record_activity(plant_id, activity_type, details)
        
        sql_result = await self.sql.record_activity(int(plant_id), activity_type, details)
        
        # Dual write activity - this is critical for event sourcing history
        if self.mode == "dual_write":
            asyncio.create_task(self._safe_algo_activity(plant_id, activity_type, details))
            
        return sql_result

    async def _safe_algo_activity(self, pid, atype, details):
        try:
            await self.algo.record_activity(pid, atype, details)
        except Exception as e:
            logger.error(f"HybridRepo: Failed to dual-write activity to Algorand: {e}")
