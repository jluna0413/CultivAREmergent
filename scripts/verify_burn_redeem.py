import asyncio
import sys
import os
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models_async.base import Base
from app.models_async.auth import User
from app.models_async.sbt import GrowJournalSBT, SBTBadgeTier
from app.services.burn_redeem_service import BurnRedeemService

# Use in-memory SQLite for testing
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

async def verify_burn_redeem():
    print("\n--- VERIFYING BURN-TO-REDEEM LOGIC (STORY 6) ---\n")
    
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # 1. Setup: User
        print(">>> SETUP: Creating User...")
        user = User(username="grower_mike", email="mike@test.com", password_hash="pw", is_active=True)
        session.add(user)
        await session.commit()
        user_id = user.id
        
        # 2. Test 1: Full Pack Consumption (10/10) -> Master Grower
        print("\n>>> TEST 1: Full Pack Consumption (10/10)")
        sbt1 = await BurnRedeemService.process_burn_redemption(
            session, user_id, "GNFT_001", "Blue Dream", seeds_planted=10, pack_size=10
        )
        print(f"Stats: {sbt1.seeds_planted}/{sbt1.pack_size} (Ratio: {sbt1.consumption_ratio})")
        print(f"Badge Tier: {sbt1.badge_tier.value}")
        
        if sbt1.badge_tier != SBTBadgeTier.MASTER_GROWER:
            print(f"[FAIL] Expected Master Grower, got {sbt1.badge_tier}")
            return
        if sbt1.consumption_ratio != 1.0:
            print(f"[FAIL] Expected Ratio 1.0, got {sbt1.consumption_ratio}")
            return
        print("[OK] Master Grower Badge Minted.")

        # 3. Test 2: Partial Consumption (5/10) -> Cultivator
        print("\n>>> TEST 2: Partial Consumption (5/10)")
        sbt2 = await BurnRedeemService.process_burn_redemption(
            session, user_id, "GNFT_002", "Sour Diesel", seeds_planted=5, pack_size=10
        )
        print(f"Stats: {sbt2.seeds_planted}/{sbt2.pack_size} (Ratio: {sbt2.consumption_ratio})")
        print(f"Badge Tier: {sbt2.badge_tier.value}")
        
        if sbt2.badge_tier != SBTBadgeTier.CULTIVATOR:
             print(f"[FAIL] Expected Cultivator, got {sbt2.badge_tier}")
             return
        print("[OK] Cultivator Badge Minted.")

        # 4. Test 3: Invalid Input (> Pack Size)
        print("\n>>> TEST 3: Invalid Input (11/10)")
        try:
            await BurnRedeemService.process_burn_redemption(
                session, user_id, "GNFT_003", "OG Kush", seeds_planted=11, pack_size=10
            )
            print("[FAIL] Should have raised ValueError")
            return
        except ValueError as e:
            print(f"[OK] Caught Expected Error: {e}")
            
    print("\n>>> SYSTEM VERIFIED SUCCESSFULLY [OK]")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_burn_redeem())
