from pydantic import BaseModel
from typing import List, Optional

class CheckoutItem(BaseModel):
    listing_id: int
    pack_size: int
    quantity: int

class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]
    shipping_address: Optional[str] = None
    payment_method: str = "card"

class CheckoutResponse(BaseModel):
    order_id: int
    total_amount: float
    status: str
    message: str
