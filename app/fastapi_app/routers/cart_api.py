from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.fastapi_app.dependencies import get_db, require_login
from app.models_async.auth import User
from app.schemas.cart import CartItemResponse, CartItemCreate, CartItemUpdate, CartResponse
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartResponse)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    items = await CartService.get_cart(db, current_user.id)
    
    # Simple total calculation
    total = 0.0
    for item in items:
        # Assuming we can access the price from the joined listing
        # Our MarketplaceListing model has pack_X_price.
        price_attr = f"pack_{item.pack_size}_price"
        price = getattr(item.listing, price_attr, 0.0) or 0.0
        total += price * item.quantity
        
        # Hydrate for schema
        if item.listing.genetics:
            item.listing.strain_name = item.listing.genetics.name
            item.listing.image_url = f"https://images.unsplash.com/photo-1603909223429-69bb7df9179c?auto=format&fit=crop&q=80&w=400&hash={item.listing.id}"

    return CartResponse(items=items, total_amount=total)

@router.post("/", response_model=CartItemResponse)
async def add_to_cart(
    request: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    return await CartService.add_item(
        db, current_user.id, request.listing_id, request.quantity, request.pack_size
    )

@router.delete("/{cart_item_id}")
async def remove_from_cart(
    cart_item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    await CartService.remove_item(db, current_user.id, cart_item_id)
    return {"status": "success"}

@router.delete("/")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    await CartService.clear_cart(db, current_user.id)
    return {"status": "success"}
