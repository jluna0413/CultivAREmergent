from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# --- DTOs (Data Transfer Objects) ---

class PlantDTO(BaseModel):
    """
    Storage-agnostic representation of a Plant.
    Used to transfer data from Repository to Business Logic / API.
    """
    id: int | str  # SQL uses int, Blockchain uses uint64 ID or TX Hash
    user_id: int | str # Blockchain might use Address string
    name: str
    status_id: int
    cultivar_id: Optional[int] = None
    zone_id: Optional[int] = None
    
    current_day: int = 0
    current_week: int = 0
    current_height: Optional[str] = None
    
    start_dt: Optional[datetime] = None
    harvest_date: Optional[datetime] = None
    harvest_weight: Optional[float] = None
    est_harvest_date: Optional[datetime] = None
    
    is_clone: bool = False
    autoflower: bool = False
    
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Relationship placeholders (names only, to keep DTO light)
    status_name: Optional[str] = None
    strain_name: Optional[str] = None
    breeder_name: Optional[str] = None
    zone_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PlantCreateDTO(BaseModel):
    """Data required to create a new plant"""
    user_id: int | str
    name: str
    cultivar_id: Optional[int] = None
    is_clone: bool = False
    parent_id: Optional[int] = None
    zone_id: Optional[int] = None
    status_id: int = 1  # Default to 'Seedling' or similar


class PlantUpdateDTO(BaseModel):
    """Data allowed to update on a plant"""
    name: Optional[str] = None
    status_id: Optional[int] = None
    zone_id: Optional[int] = None
    current_height: Optional[str] = None
    harvest_weight: Optional[float] = None
    harvest_date: Optional[datetime] = None
    image_url: Optional[str] = None


class ActivityDTO(BaseModel):
    """Immutable record of an event for Blockchain logging"""
    id: Optional[str] = None # Could be TX hash or SQL ID
    plant_id: int | str
    activity_type: str
    details: Dict[str, Any]
    timestamp: datetime
    
    # Blockchain specific metadata
    tx_hash: Optional[str] = None
    block_round: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# --- Repository Interface ---

class PlantRepository(ABC):
    """
    Abstract interface for Plant data access.
    Implementations: SQLPlantRepository, AlgorandPlantRepository
    """

    @abstractmethod
    async def create(self, plant_data: PlantCreateDTO) -> PlantDTO:
        """Create a new plant"""
        pass

    @abstractmethod
    async def get_by_id(self, plant_id: int | str) -> Optional[PlantDTO]:
        """Get plant by unique identifier"""
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int | str, skip: int = 0, limit: int = 100) -> List[PlantDTO]:
        """Get all plants belonging to a user"""
        pass

    @abstractmethod
    async def update(self, plant_id: int | str, update_data: PlantUpdateDTO) -> Optional[PlantDTO]:
        """Update existing plant details"""
        pass

    @abstractmethod
    async def delete(self, plant_id: int | str) -> bool:
        """Delete a plant (or archive on blockchain)"""
        pass

    @abstractmethod
    async def record_activity(self, plant_id: int | str, activity: ActivityDTO) -> ActivityDTO:
        """Log an immutable activity/event for the plant"""
        pass
