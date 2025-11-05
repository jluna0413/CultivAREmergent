"""Pydantic models for Cultivars domain."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class CultivarBase(BaseModel):
    """Base cultivar model with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Cultivar name")
    breeder_id: Optional[int] = Field(None, description="Breeder ID")
    indica: int = Field(0, ge=0, le=100, description="Indica percentage (0-100)")
    sativa: int = Field(0, ge=0, le=100, description="Sativa percentage (0-100)")
    autoflower: bool = Field(False, description="Whether cultivar is autoflower")
    cycle_time: Optional[int] = Field(None, ge=1, le=365, description="Flowering cycle time in days")
    seed_count: Optional[int] = Field(None, ge=1, description="Average seed count per plant")
    url: Optional[str] = Field(None, description="Cultivar information URL")
    description: Optional[str] = Field(None, max_length=1000, description="Cultivar description")

    @validator('sativa')
    def validate_sativa_percentage(cls, v, values):
        """Validate sativa percentage against indica for hybrid classification."""
        if 'indica' in values and v + values['indica'] > 110:  # Allow small rounding error
            raise ValueError('Combined indica + sativa percentage cannot exceed 100%')
        return v


class CultivarCreate(CultivarBase):
    """Model for creating a new cultivar."""
    created_by: Optional[int] = Field(None, description="User ID who created the cultivar")


class CultivarUpdate(BaseModel):
    """Model for updating an existing cultivar."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    breeder_id: Optional[int] = None
    indica: Optional[int] = Field(None, ge=0, le=100)
    sativa: Optional[int] = Field(None, ge=0, le=100)
    autoflower: Optional[bool] = None
    cycle_time: Optional[int] = Field(None, ge=1, le=365)
    seed_count: Optional[int] = Field(None, ge=1)
    url: Optional[str] = None
    description: Optional[str] = Field(None, max_length=1000)

    @validator('sativa')
    def validate_sativa_percentage(cls, v, values):
        """Validate sativa percentage against indica for hybrid classification."""
        if v is not None and 'indica' in values and values['indica'] is not None:
            if v + values['indica'] > 110:
                raise ValueError('Combined indica + sativa percentage cannot exceed 100%')
        return v


class CultivarResponse(CultivarBase):
    """Model for cultivar response with computed fields."""
    id: int = Field(..., description="Cultivar ID")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    created_by: Optional[int] = Field(None, description="User ID who created the cultivar")
    
    # Computed fields
    type: str = Field(..., description="Cultivar type (indica/sativa/hybrid)")
    breeder_name: Optional[str] = Field(None, description="Breeder name")

    class Config:
        from_attributes = True
        use_enum_values = True


class CultivarListResponse(BaseModel):
    """Model for paginated cultivar list response."""
    items: List[CultivarResponse] = Field(..., description="List of cultivars")
    total: int = Field(..., description="Total number of cultivars")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class CultivarFilters(BaseModel):
    """Model for cultivar filtering parameters."""
    breeder_id: Optional[int] = None
    cultivar_type: Optional[str] = Field(None, description="Filter by cultivar type: indica, sativa, hybrid")
    autoflower: Optional[bool] = None
    min_cycle_time: Optional[int] = Field(None, ge=1, description="Minimum cycle time in days")
    max_cycle_time: Optional[int] = Field(None, ge=1, description="Maximum cycle time in days")
    search: Optional[str] = Field(None, description="Search term for name/description")


class CultivarStats(BaseModel):
    """Model for cultivar statistics."""
    total_cultivars: int = Field(..., description="Total number of cultivars")
    indica_count: int = Field(..., description="Number of indica cultivars")
    sativa_count: int = Field(..., description="Number of sativa cultivars")
    hybrid_count: int = Field(..., description="Number of hybrid cultivars")
    autoflower_count: int = Field(..., description="Number of autoflower cultivars")
    average_cycle_time: Optional[float] = Field(None, description="Average cycle time in days")