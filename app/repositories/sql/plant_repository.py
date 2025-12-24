from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.repositories.interfaces import (
    PlantRepository, 
    PlantDTO, 
    PlantCreateDTO, 
    PlantUpdateDTO,
    ActivityDTO
)
from app.models_async.grow import Plant, Cultivar
from app.models_async.activities import PlantActivity

class SQLPlantRepository(PlantRepository):
    """
    PostgreSQL/SQLite implementation using SQLAlchemy.
    Used for 'sql_only' and 'dual_write' modes.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, plant_data: PlantCreateDTO) -> PlantDTO:
        # Convert DTO to ORM model
        new_plant = Plant(
            user_id=plant_data.user_id,
            name=plant_data.name,
            cultivar_id=plant_data.cultivar_id,
            is_clone=plant_data.is_clone,
            parent_id=plant_data.parent_id,
            zone_id=plant_data.zone_id,
            status_id=plant_data.status_id
        )
        
        self.session.add(new_plant)
        await self.session.commit()
        await self.session.refresh(new_plant)
        
        # Eager load relationships for the DTO properties if needed, 
        # or rely on lazy loading if session is active (but prefer explicit for async)
        # For simplicity in create, we just return the basic data
        return PlantDTO.model_validate(new_plant)

    async def get_by_id(self, plant_id: int) -> Optional[PlantDTO]:
        # Eager load relationships used in properties
        stmt = (
            select(Plant)
            .options(
                selectinload(Plant.status),
                selectinload(Plant.cultivar).selectinload(Cultivar.breeder),
                selectinload(Plant.zone),
                selectinload(Plant.images)
            )
            .where(Plant.id == plant_id)
        )
        result = await self.session.execute(stmt)
        plant = result.scalar_one_or_none()
        
        if plant:
            return PlantDTO.model_validate(plant)
        return None

    async def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[PlantDTO]:
        stmt = (
            select(Plant)
            .options(
                selectinload(Plant.status),
                selectinload(Plant.cultivar).selectinload(Cultivar.breeder),
                selectinload(Plant.zone)
            )
            .where(Plant.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        plants = result.scalars().all()
        
        return [PlantDTO.model_validate(p) for p in plants]

    async def update(self, plant_id: int, update_data: PlantUpdateDTO) -> Optional[PlantDTO]:
        # Filter out None values to only update what's provided
        update_dict = update_data.model_dump(exclude_unset=True)
        
        if not update_dict:
            return await self.get_by_id(plant_id)

        stmt = (
            update(Plant)
            .where(Plant.id == plant_id)
            .values(**update_dict)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(stmt)
        
        if result.rowcount == 0:
            return None
            
        await self.session.commit()
        
        # Return updated object
        return await self.get_by_id(plant_id)

    async def delete(self, plant_id: int) -> bool:
        stmt = delete(Plant).where(Plant.id == plant_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def record_activity(self, plant_id: int, activity: ActivityDTO) -> ActivityDTO:
        # Resolve activity type string to ID
        from app.models_async.activities import ActivityType
        stmt = select(ActivityType).where(ActivityType.name == activity.activity_type)
        result = await self.session.execute(stmt)
        act_type_obj = result.scalar_one_or_none()
        
        if not act_type_obj:
            # Create if not exists (or could raise error)
            act_type_obj = ActivityType(name=activity.activity_type, category="plant", is_system=False)
            self.session.add(act_type_obj)
            await self.session.flush()  # get ID
            
        new_activity = PlantActivity(
            plant_id=plant_id,
            activity_type_id=act_type_obj.id,
            activity_name=activity.activity_type,
            details=activity.details
        )
        self.session.add(new_activity)
        await self.session.commit()
        await self.session.refresh(new_activity)
        
        self.session.add(new_activity)
        await self.session.commit()
        await self.session.refresh(new_activity)
        
        # Manually map ORM to DTO due to field name differences
        return ActivityDTO(
            id=str(new_activity.id),
            plant_id=new_activity.plant_id,
            activity_type=new_activity.activity_name,
            details=new_activity.details or {},
            timestamp=new_activity.date or datetime.utcnow(),
            # Blockchain metadata is None for SQL events
        )
