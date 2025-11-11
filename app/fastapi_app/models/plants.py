"""Pydantic models for Plants domain."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class PlantBase(BaseModel):
    """Base plant model with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Plant name")
    cultivar_id: int = Field(..., description="Cultivar ID")
    zone_id: Optional[int] = Field(None, description="Zone ID")
    status: str = Field("seedling", description="Current growth status")
    start_date: datetime = Field(default_factory=datetime.utcnow, description="Start date of the plant's life")
    description: Optional[str] = Field(None, max_length=1000, description="Plant description")

class PlantCreate(PlantBase):
    """Model for creating a new plant."""
    user_id: int = Field(..., description="User ID of the plant owner")

class PlantUpdate(BaseModel):
    """Model for updating an existing plant."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    cultivar_id: Optional[int] = None
    zone_id: Optional[int] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    description: Optional[str] = Field(None, max_length=1000)

class PlantResponse(PlantBase):
    """Model for plant response with computed fields."""
    id: int = Field(..., description="Plant ID")
    user_id: int = Field(..., description="User ID of the plant owner")
    cultivar_name: str = Field(..., description="Cultivar name")
    zone_name: Optional[str] = Field(None, description="Zone name")
    age_days: int = Field(..., description="Age of the plant in days")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class PlantListResponse(BaseModel):
    """Model for paginated plant list response."""
    items: List[PlantResponse] = Field(..., description="List of plants")
    total: int = Field(..., description="Total number of plants")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")
