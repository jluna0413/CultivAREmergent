"""Pydantic models for Breeders domain."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class BreederBase(BaseModel):
    """Base breeder model with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Breeder name")
    country: Optional[str] = Field(None, max_length=100, description="Breeder country of origin")
    website: Optional[str] = Field(None, max_length=255, description="Breeder website URL")
    seedfinder_id: Optional[str] = Field(None, max_length=100, description="SeedFinder API identifier")
    description: Optional[str] = Field(None, max_length=2000, description="Detailed breeder information")

    @validator('website')
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Website must be a valid URL (e.g., http://example.com)')
        return v


class BreederCreate(BreederBase):
    """Model for creating a new breeder."""
    pass


class BreederUpdate(BaseModel):
    """Model for updating an existing breeder."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    country: Optional[str] = Field(None, max_length=100, description="Breeder country of origin")
    website: Optional[str] = Field(None, max_length=255, description="Breeder website URL")
    seedfinder_id: Optional[str] = Field(None, max_length=100, description="SeedFinder API identifier")
    description: Optional[str] = Field(None, max_length=2000, description="Detailed breeder information")

    @validator('website')
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Website must be a valid URL (e.g., http://example.com)')
        return v


class BreederResponse(BreederBase):
    """Model for breeder response with computed fields."""
    id: int = Field(..., description="Breeder ID")
    
    # Computed fields
    cultivar_count: int = Field(0, description="Number of cultivars from this breeder")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class BreederListResponse(BaseModel):
    """Model for paginated breeder list response."""
    items: List[BreederResponse] = Field(..., description="List of breeders")
    total: int = Field(..., description="Total number of breeders")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class BreederCreateResponse(BaseModel):
    """Response model for breeder creation API."""
    message: str
    status: str
    breeder_id: int


class BreederUpdateResponse(BaseModel):
    """Response model for breeder update API."""
    message: str
    status: str


class BreederDeleteResponse(BaseModel):
    """Response model for breeder deletion API."""
    message: str
    status: str


class BreederStats(BaseModel):
    """Model for breeder statistics."""
    total_breeders: int = Field(..., description="Total number of breeders")
    most_prolific_breeder: Optional[str] = Field(None, description="Breeder with most cultivars")
    total_cultivars_from_top_breeder: Optional[int] = Field(None, description="Cultivar count for top breeder")
