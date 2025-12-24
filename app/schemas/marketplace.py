from pydantic import BaseModel, Field, conlist
from typing import List, Optional
from datetime import datetime
from app.fastapi_app.models.users import UserResponse

class PackPricing(BaseModel):
    """Configuration for a specific pack size."""
    price: Optional[float] = Field(None, description="Price for this pack size (e.g., 50.0). None if not offered.")
    available_quantity: int = Field(0, description="Number of packs available for this size.")

class GNFTListingBase(BaseModel):
    """Base fields for GNFT Listing."""
    genetics_id: int = Field(..., description="ID of the UserGenetics to list.")
    listing_title: str = Field(..., max_length=150, description="Title of the listing.")
    description: Optional[str] = Field(None, description="Detailed description of the listing.")
    
    # Pricing/Availability per pack size
    pack_3_config: Optional[PackPricing] = Field(None)
    pack_5_config: Optional[PackPricing] = Field(None)
    pack_6_config: Optional[PackPricing] = Field(None)
    pack_10_config: Optional[PackPricing] = Field(None)
    pack_12_config: Optional[PackPricing] = Field(None)
    
    is_active: bool = Field(True, description="Whether the listing is visible in the marketplace.")

class GNFTListingCreate(GNFTListingBase):
    """Schema for creating a new listing."""
    pass

class GNFTListingUpdate(BaseModel):
    """Schema for updating a listing."""
    listing_title: Optional[str] = None
    description: Optional[str] = None
    
    pack_3_config: Optional[PackPricing] = None
    pack_5_config: Optional[PackPricing] = None
    pack_6_config: Optional[PackPricing] = None
    pack_10_config: Optional[PackPricing] = None
    pack_12_config: Optional[PackPricing] = None
    
    is_active: Optional[bool] = None

class GNFTListingResponse(GNFTListingBase):
    """Schema for returning a listing."""
    id: int
    breeder_id: int
    breeder_name: Optional[str] = None # Or full breeder object?
    
    # Flattened for response or keep structured?
    # Keeping structured 'config' assumes FE handles it.
    # But DB has flattened columns (pack_3_price, pack_3_available).
    # Services will need to map between flat DB columns and this structured Schema.
    
    total_seeds_available: int
    seeds_sold: int
    
    created_at: datetime
    updated_at: datetime

    # Extended fields from Genetics/DB
    strain_name: Optional[str] = None
    thc_percentage: Optional[float] = None
    is_indica: Optional[bool] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
