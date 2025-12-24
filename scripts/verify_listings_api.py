import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.config import Config
from app.models_async import User, MarketplaceBreeder, UserGenetics, GNFTListing, GeneticsType

async def verify_listings_flow():
    """
    Simulation of the Listings Flow:
    1. Setup: Create Test User, Test Breeder, Test Genetics.
    2. Test: Call Service to Create Listing.
    3. Verify: Check DB for listing and flat columns.
    4. Cleanup.
    """
    print("--- Verifying Marketplace Listings Flow ---")
    
    engine = create_async_engine(Config.get_async_database_uri())
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # 1. Setup Data
        TEST_EMAIL = "verify_breeder@test.com"
        
        # Cleanup existing
        stmt = select(User).where(User.email == TEST_EMAIL)
        exist = (await session.execute(stmt)).scalar_one_or_none()
        if exist:
            # Drop dependencies?
            # Cascades should handle it usually, but let's be safe
            await session.delete(exist)
            await session.commit()
            print("Cleaned up previous test user.")

        # Create User
        user = User(
            email=TEST_EMAIL, 
            username="verify_user",
            password_hash="hashed_pw", 
            is_active=True, 
            is_verified_breeder=True
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        # Create Breeder Profile
        breeder = MarketplaceBreeder(
            user_id=user.id,
            breeder_name="Test Verification Breeder",
            is_verified=True
        )
        session.add(breeder)
        await session.commit()
        await session.refresh(breeder)
        
        # Create User Genetics
        genetics = UserGenetics(
            user_id=user.id,
            name="Verification Kush",
            genetics_type=GeneticsType.MOTHER,
            is_active=True
        )
        session.add(genetics)
        await session.commit()
        await session.refresh(genetics)
        
        print(f"Setup Complete: User ID {user.id}, Breeder ID {breeder.id}, Genetics ID {genetics.id}")

        # 2. Simulate Service Call (Direct Service Call for functional test)
        # We test the service logic. API Router just wraps this.
        from app.services.marketplace_service import MarketplaceService
        from app.schemas.marketplace import GNFTListingCreate, PackPricing
        
        listing_input = GNFTListingCreate(
            genetics_id=genetics.id,
            listing_title="Verification Kush Drops",
            description="Limited edition test drop.",
            
            pack_5_config=PackPricing(price=50.0, available_quantity=10),
            pack_10_config=PackPricing(price=90.0, available_quantity=5),
            
            is_active=True
        )
        
        try:
            listing = await MarketplaceService.create_listing(session, user.id, listing_input)
            print(f"Listing Created: ID {listing.id}")
            print(f"Total Seeds: {listing.total_seeds_available} (Should be 5*10 + 10*5 = 100)")
            
            if listing.total_seeds_available != 100:
                print("❌ ERROR: Total seed calculation failed.")
            else:
                print("✅ Seed calculation correct.")
                
            if listing.pack_5_price == 50.0 and listing.pack_10_available == 5:
                print("✅ Columns flattened correctly.")
            else:
                 print("❌ ERROR: Column flattening failed.")
                 
        except Exception as e:
            print(f"❌ Service Error: {e}")
            import traceback
            traceback.print_exc()

        # Cleanup
        # await session.delete(user) # Keep for inspection if needed, or uncomment to clean
        # await session.commit()
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(verify_listings_flow())
