from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from typing import List, Optional
from datetime import datetime

from app.models_async import GNFTListing, MarketplaceBreeder, UserGenetics, GNFTPack
from app.schemas.marketplace import GNFTListingCreate, GNFTListingUpdate, GNFTListingResponse

class MarketplaceService:
    @staticmethod
    async def create_listing(session: AsyncSession, user_id: int, listing_data: GNFTListingCreate) -> GNFTListing:
        """
        Create a new GNFT listing.
        Requires user to be a verified breeder and own the genetics.
        """
        # 1. Verify Breeder Status
        stmt = select(MarketplaceBreeder).where(MarketplaceBreeder.user_id == user_id)
        result = await session.execute(stmt)
        breeder = result.scalar_one_or_none()
        
        if not breeder:
            raise ValueError("User is not a registered breeder.")
            
        # 2. Verify Genetics Ownership
        stmt = select(UserGenetics).where(
            (UserGenetics.id == listing_data.genetics_id) & 
            (UserGenetics.user_id == user_id)
        )
        result = await session.execute(stmt)
        genetics = result.scalar_one_or_none()
        
        if not genetics:
            raise ValueError("Genetics not found or not owned by user.")
            
        # 3. Calculate Total Seeds & Flatten Config
        total_seeds = 0
        db_dump = listing_data.model_dump(exclude={'pack_3_config', 'pack_5_config', 'pack_6_config', 'pack_10_config', 'pack_12_config'})
        
        # Helper to process pack config
        def process_config(config, size):
            nonlocal total_seeds
            if config and config.price is not None:
                total_seeds += config.available_quantity * size
                return config.price, config.available_quantity
            return None, 0

        p3_price, p3_qty = process_config(listing_data.pack_3_config, 3)
        p5_price, p5_qty = process_config(listing_data.pack_5_config, 5)
        p6_price, p6_qty = process_config(listing_data.pack_6_config, 6)
        p10_price, p10_qty = process_config(listing_data.pack_10_config, 10)
        p12_price, p12_qty = process_config(listing_data.pack_12_config, 12)
        
        # 4. Create DB Object
        new_listing = GNFTListing(
            breeder_id=breeder.id,
            total_seeds_available=total_seeds,
            seeds_sold=0,
            
            # Pack Configs
            pack_3_price=p3_price, pack_3_available=p3_qty,
            pack_5_price=p5_price, pack_5_available=p5_qty,
            pack_6_price=p6_price, pack_6_available=p6_qty,
            pack_10_price=p10_price, pack_10_available=p10_qty,
            pack_12_price=p12_price, pack_12_available=p12_qty,
            
            **db_dump
        )
        
        session.add(new_listing)
        await session.commit()
        await session.refresh(new_listing)
        return new_listing

    @staticmethod
    async def get_listings(
        session: AsyncSession, 
        skip: int = 0, 
        limit: int = 20,
        breeder_id: Optional[int] = None
    ) -> List[GNFTListing]:
        """Get active listings with genetics details."""
        from sqlalchemy.orm import joinedload
        
        stmt = select(GNFTListing).options(
            joinedload(GNFTListing.genetics),
            joinedload(GNFTListing.breeder)
        ).where(GNFTListing.is_active == True)
        
        if breeder_id:
            stmt = stmt.where(GNFTListing.breeder_id == breeder_id)
            
        stmt = stmt.order_by(desc(GNFTListing.created_at)).offset(skip).limit(limit)
        
        result = await session.execute(stmt)
        listings = result.scalars().all()
        
        # Hydrate the extended fields explicitly if needed, or rely on Pydantic `from_attributes`
        # interacting with the loaded SQLAlchemy models.
        # However, `strain_name` is in UserGenetics (namespaced `genetics.name`).
        # The Schema expects `strain_name` at root. Pydantic v2 `from_attributes` might not auto-flatten.
        # Let's attach them to the object to be safe or simple wrapper.
        
        for listing in listings:
            if listing.genetics:
                listing.strain_name = listing.genetics.name
                listing.thc_percentage = listing.genetics.thc_percentage
                # Approximate indica calculation
                if listing.genetics.indica_percentage:
                    listing.is_indica = listing.genetics.indica_percentage >= 50.0
                else:
                    listing.is_indica = None
                
                # Placeholder for image until DB support
                # Generate a random unsplash image based on ID -> Deterministic
                listing.image_url = f"https://images.unsplash.com/photo-1603909223429-69bb7df9179c?auto=format&fit=crop&q=80&w=400&hash={listing.id}"
                
            if listing.breeder:
                 listing.breeder_name = listing.breeder.breeder_name

        return listings

    @staticmethod
    async def get_listing(session: AsyncSession, listing_id: int) -> Optional[GNFTListing]:
        stmt = select(GNFTListing).where(GNFTListing.id == listing_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def link_to_global_breeder(session: AsyncSession, marketplace_breeder_id: int) -> bool:
        """
        Attempts to link a marketplace breeder to a global master breeder record
        (ingested from SeedFinder) based on name matching.
        """
        from app.models_async.grow import Breeder
        
        # 1. Get Marketplace Breeder
        stmt = select(MarketplaceBreeder).where(MarketplaceBreeder.id == marketplace_breeder_id)
        result = await session.execute(stmt)
        m_breeder = result.scalar_one_or_none()
        
        if not m_breeder or m_breeder.breeder_id:
            return False
            
        # 2. Search for Global Breeder by name
        stmt = select(Breeder).where(Breeder.name == m_breeder.breeder_name)
        result = await session.execute(stmt)
        g_breeder = result.scalar_one_or_none()
        
        if g_breeder:
            m_breeder.breeder_id = g_breeder.id
            await session.commit()
            return True
            
        return False

    @staticmethod
    async def get_breeder_for_strain(session: AsyncSession, strain_name: str) -> Optional["Breeder"]:
        """
        Finds the global Breeder record associated with a strain/cultivar name.
        Used by the Trust Engine to verify breeder authenticity.
        """
        from app.models_async.grow import Breeder, Cultivar
        
        # Look up cultivar by name
        stmt = select(Cultivar).where(Cultivar.name == strain_name)
        result = await session.execute(stmt)
        cultivar = result.scalar_one_or_none()
        
        if cultivar and cultivar.breeder_id:
            # Get the breeder
            stmt = select(Breeder).where(Breeder.id == cultivar.breeder_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        
        return None
