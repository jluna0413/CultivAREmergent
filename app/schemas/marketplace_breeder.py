
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class MarketplaceBreederBase(BaseModel):
    breeder_name: str
    bio: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    
    # Blockchain
    algorand_address: Optional[str] = None
    
    # Payment
    payment_address: Optional[str] = None
    payment_method: Optional[str] = None

class MarketplaceBreederCreate(MarketplaceBreederBase):
    pass

class MarketplaceBreederResponse(MarketplaceBreederBase):
    id: int
    user_id: int
    is_verified: bool
    total_sales: int
    rating_avg: int
    current_tier: str
    month_sales: int
    active_commission_rate: float # Computed, not DB
    created_at: datetime
    
    class Config:
        from_attributes = True
