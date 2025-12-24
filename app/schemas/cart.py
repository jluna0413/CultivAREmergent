from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.marketplace import GNFTListingResponse

class CartItemBase(BaseModel):
    listing_id: int
    quantity: int
    pack_size: int = 5

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(CartItemBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    listing: Optional[GNFTListingResponse] = None

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_amount: float
