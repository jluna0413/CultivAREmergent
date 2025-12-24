from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models_async.cart import CartItem
from app.models_async.gnft import GNFTListing

class CartService:
    @staticmethod
    async def get_cart(db: AsyncSession, user_id: int) -> List[CartItem]:
        stmt = select(CartItem).options(
            joinedload(CartItem.listing).joinedload(GNFTListing.genetics)
        ).where(CartItem.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def add_item(
        db: AsyncSession, 
        user_id: int, 
        listing_id: int, 
        quantity: int = 1, 
        pack_size: int = 5
    ) -> CartItem:
        # Check if already exists
        stmt = select(CartItem).where(
            CartItem.user_id == user_id, 
            CartItem.listing_id == listing_id,
            CartItem.pack_size == pack_size
        )
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        
        if item:
            item.quantity += quantity
        else:
            item = CartItem(
                user_id=user_id,
                listing_id=listing_id,
                quantity=quantity,
                pack_size=pack_size
            )
            db.add(item)
            
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def remove_item(db: AsyncSession, user_id: int, cart_item_id: int):
        stmt = select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == user_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        if item:
            await db.delete(item)
            await db.commit()

    @staticmethod
    async def clear_cart(db: AsyncSession, user_id: int):
        from sqlalchemy import delete
        stmt = delete(CartItem).where(CartItem.user_id == user_id)
        await db.execute(stmt)
        await db.commit()
