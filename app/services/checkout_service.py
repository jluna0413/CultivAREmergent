from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models_async.gnft import GNFTListing, GNFTPack
from app.models_async.sales import SalesTransaction, TransactionStatus
from app.schemas.checkout import CheckoutRequest, CheckoutResponse, CheckoutItem
import random

class CheckoutService:
    @staticmethod
    async def process_checkout(
        db: AsyncSession, 
        user_id: int, 
        request: CheckoutRequest
    ) -> CheckoutResponse:
        """
        Process a checkout request.
        Simplification for Phase 2:
        - Verify stock.
        - Create transaction.
        - Create (mock) packs for the user.
        """
        total_amount = 0.0
        
        # 1. Validate items and calculate total
        for item in request.items:
            listing_stmt = select(GNFTListing).where(GNFTListing.id == item.listing_id)
            result = await db.execute(listing_stmt)
            listing = result.scalar_one_or_none()
            
            if not listing:
                raise ValueError(f"Listing {item.listing_id} not found")
            
            if not listing.is_active:
                raise ValueError(f"Listing {listing.listing_title} is no longer active")

            # Check specific pack size availability
            attr_name = f"pack_{item.pack_size}_available"
            price_name = f"pack_{item.pack_size}_price"
            
            if not hasattr(listing, attr_name):
                raise ValueError(f"Pack size {item.pack_size} not supported for this listing")
            
            available = getattr(listing, attr_name)
            if available < item.quantity:
                raise ValueError(f"Insufficient stock for {listing.listing_title} ({item.pack_size} pack)")
            
            price = getattr(listing, price_name) or 0.0
            total_amount += price * item.quantity

        # 2. Create Sales Transaction
        # For simplicity, we assume breeder_id from the first listing for the transaction record
        # In a multi-breeder cart, you'd have multiple transactions or one order with multiple items.
        # Here we just record one main transaction.
        first_listing_id = request.items[0].listing_id
        res = await db.execute(select(GNFTListing).where(GNFTListing.id == first_listing_id))
        primary_listing = res.scalar_one()

        transaction = SalesTransaction(
            buyer_user_id=user_id,
            seller_user_id=primary_listing.breeder_id,
            total_amount=total_amount,
            currency="USD",
            payment_method=request.payment_method,
            transaction_reference=f"MOCK_TX_{random.randint(1000, 9999)}",
            status=TransactionStatus.COMPLETED
        )
        db.add(transaction)
        
        # 3. Update stock and Create packs
        for item in request.items:
            res = await db.execute(select(GNFTListing).where(GNFTListing.id == item.listing_id))
            listing = res.scalar_one()
            
            attr_name = f"pack_{item.pack_size}_available"
            current_val = getattr(listing, attr_name)
            setattr(listing, attr_name, current_val - item.quantity)
            listing.seeds_sold += (item.pack_size * item.quantity)
            
            # Create GNFTPacks for the user
            for _ in range(item.quantity):
                pack = GNFTPack(
                    exclusive_drop_id=listing.exclusive_drop_id,
                    listing_id=listing.id,
                    pack_size=item.pack_size,
                    pack_number=random.randint(1, 1000), # Mock
                    current_owner_id=user_id,
                    first_minter_user_id=user_id,
                    pack_asset_id=random.randint(1000000, 9999999) # Mock ASA ID
                )
                db.add(pack)

        await db.commit()
        
        return CheckoutResponse(
            order_id=transaction.id,
            total_amount=total_amount,
            status="success",
            message="Order placed successfully"
        )
