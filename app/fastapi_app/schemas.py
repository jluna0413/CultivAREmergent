"""
Plant Schemas for FastAPI
Pydantic models for plant-related API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class PlantType(str, Enum):
    """Enum for plant types"""
    REGULAR = "regular"
    AUTOFLOWER = "autoflower"
    FEMINIZED = "feminized"

class PlantStatus(str, Enum):
    """Enum for plant status"""
    SEEDLING = "seedling"
    VEGETATIVE = "vegetative" 
    FLOWERING = "flowering"
    HARVESTED = "harvested"
    CULLED = "culled"

class PlantCreate(BaseModel):
    """Schema for creating a new plant"""
    name: str = Field(..., min_length=1, max_length=100, description="Plant name")
    description: Optional[str] = Field(None, max_length=1000, description="Plant description")
    status_id: int = Field(..., description="Status ID")
    cultivar_id: Optional[int] = Field(None, description="Cultivar ID")
    is_clone: bool = Field(False, description="Whether plant is a clone")
    autoflower: bool = Field(False, description="Whether plant is autoflower")
    start_dt: Optional[datetime] = Field(None, description="Plant start date")

class PlantUpdate(BaseModel):
    """Schema for updating an existing plant"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Plant name")
    description: Optional[str] = Field(None, max_length=1000, description="Plant description")
    status_id: Optional[int] = Field(None, description="Status ID")
    cultivar_id: Optional[int] = Field(None, description="Cultivar ID")
    is_clone: Optional[bool] = Field(None, description="Whether plant is a clone")
    autoflower: Optional[bool] = Field(None, description="Whether plant is autoflower")
    last_water_date: Optional[datetime] = Field(None, description="Last watered date")
    last_feed_date: Optional[datetime] = Field(None, description="Last fed date")
    harvest_date: Optional[datetime] = Field(None, description="Harvest date")

class PlantResponse(BaseModel):
    """Schema for plant response"""
    id: int
    name: str
    description: Optional[str]
    status_id: int
    cultivar_id: Optional[int]
    is_clone: bool
    autoflower: bool
    start_dt: Optional[datetime]
    last_water_date: Optional[datetime]
    last_feed_date: Optional[datetime]
    harvest_date: Optional[datetime]
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class PlantListResponse(BaseModel):
    """Schema for paginated plant list response"""
    items: list[PlantResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool

class PlantStats(BaseModel):
    """Schema for plant statistics"""
    total_plants: int
    active_plants: int
    clones: int
    harvested: int
