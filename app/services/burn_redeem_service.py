import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models_async.sbt import GrowJournalSBT, SBTBadgeTier

class BurnRedeemService:
    """
    Handles the logic for Burning G-NFTs and Redeeming 'Grow Journal' SBTs.
    Logic:
    - User burns G-NFT (simulated or verified on-chain).
    - User claims 'seeds_planted' vs 'pack_size'.
    - Service validates and mints SBT.
    """

    @staticmethod
    async def process_burn_redemption(
        db: AsyncSession, 
        user_id: int, 
        burned_gnft_id: str, 
        strain_name: str, 
        seeds_planted: int, 
        pack_size: int
    ) -> GrowJournalSBT:
        """
        Process a specific Redemption request.
        """
        if seeds_planted > pack_size:
            raise ValueError("Seeds planted cannot exceed pack size.")
        
        if pack_size <= 0:
             raise ValueError("Pack size must be > 0")

        # Calculate Consumption Ratio
        ratio = float(seeds_planted) / float(pack_size)
        
        # Determine Badge Tier
        tier = SBTBadgeTier.CULTIVATOR
        if ratio >= 1.0:
            tier = SBTBadgeTier.MASTER_GROWER
        elif ratio < 0.1:
            tier = SBTBadgeTier.NOVICE
            
        # Create SBT Record
        sbt = GrowJournalSBT(
            user_id=user_id,
            burned_gnft_id=burned_gnft_id,
            strain_name=strain_name,
            pack_size=pack_size,
            seeds_planted=seeds_planted,
            consumption_ratio=ratio,
            badge_tier=tier,
            sbt_asa_id=f"SBT_MOCK_{burned_gnft_id}", # Mock Algo Asset ID
            mint_tx_id=f"TX_MINT_{burned_gnft_id}"   # Mock TX
        )
        
        db.add(sbt)
        await db.commit()
        
        # In a real app, this would trigger the Algo smart contract mint()
        # await BlockchainService.mint_sbt(address, metadata=...)
        
        return sbt

    @staticmethod
    async def get_user_sbts(db: AsyncSession, user_id: int):
         stmt = select(GrowJournalSBT).where(GrowJournalSBT.user_id == user_id)
         result = await db.execute(stmt)
         return result.scalars().all()
