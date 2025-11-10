"""Pydantic models for Clones domain."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class CloneBase(BaseModel):
    """Base clone model with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Clone name")
    parent_plant_id: int = Field(..., description="ID of the parent plant")
    zone_id: Optional[int] = Field(None, description="Zone ID")
    status: str = Field("cutting", description="Current status of the clone")
    cloning_date: datetime = Field(default_factory=datetime.utcnow, description="Date the clone was taken")
    description: Optional[str] = Field(None, max_length=1000, description="Clone description")

class CloneCreate(CloneBase):
    """Model for creating a new clone."""
    user_id: int = Field(..., description="User ID of the clone owner")

class CloneUpdate(BaseModel):
    """Model for updating an existing clone."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    zone_id: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = Field(None, max_length=1000)

class CloneResponse(CloneBase):
    """Model for clone response with computed fields."""
    id: int = Field(..., description="Clone ID")
    user_id: int = Field(..., description="User ID of the clone owner")
    parent_plant_name: str = Field(..., description="Name of the parent plant")
    zone_name: Optional[str] = Field(None, description="Zone name")
    age_days: int = Field(..., description="Age of the clone in days")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class CloneListResponse(BaseModel):
    """Model for paginated clone list response."""
    items: List[CloneResponse] = Field(..., description="List of clones")
    total: int = Field(..., description="Total number of clones")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")
