import asyncio
import sys
import os
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models_async.base import Base
from app.models_async.breeders import MarketplaceBreeder
from app.models_async.auth import User 
from app.services.commission_service import CommissionService

# Use in-memory SQLite for testing
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

async def verify_commission_system():
    print("\n--- VERIFYING TIERED COMMISSION SYSTEM (MONTHLY) ---\n")
    
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # 1. Setup Data
        print(">>> SETUP: Creating Test Breeder (Starter Tier)...")
        user = User(
            username="test_breeder", 
            email="breeder@test.com", 
            password_hash="pw_hash_mock", 
            is_active=True, 
            is_verified_breeder=True
        )
        session.add(user)
        await session.flush()
        
        breeder = MarketplaceBreeder(
            user_id=user.id,
            breeder_name="StarterBreeder",
            is_verified=True,
            current_tier="Starter",
            month_sales=0,
            active_buffs="[]",
            total_sales=0,
            rating_avg=500 
        )
        session.add(breeder)
        await session.commit()
        breeder_id = breeder.id
        
        # 2. Verify Initial Fee (Starter = 25%)
        fee_1 = await CommissionService.calculate_commission(session, breeder_id)
        print(f"Initial Fee (Starter): {fee_1 * 100}%")
        if fee_1 != 0.25:
            print(f"[FAIL] Initial Fee Incorrect (Expected 25.0%, Got {fee_1*100}%)")
            return
        print("[OK] Initial Fee Verified.")
        
        # 3. Simulate Progression to Mover (10 Monthly Sales)
        print("\n>>> SIMULATION: Processing 10 Sales...")
        for _ in range(10):
            await CommissionService.update_breeder_metrics(session, breeder_id, 5000) 
            
        await session.refresh(breeder)
        print(f"Current Monthly Sales: {breeder.month_sales}")
        print(f"Current Tier: {breeder.current_tier}")
        
        if breeder.current_tier != "Mover":
            print(f"[FAIL] Tier Promotion Failed (Expected 'Mover', Got '{breeder.current_tier}')")
            return
        
        # Verify New Fee (Mover = 20%)
        fee_2 = await CommissionService.calculate_commission(session, breeder_id)
        print(f"New Fee (Mover): {fee_2 * 100}%")
        if fee_2 != 0.20:
             print(f"[FAIL] Promoted Fee Incorrect (Expected 20.0%, Got {fee_2*100}%)")
             return
        print("[OK] Tier Promotion & Fee Verified.")
             
        # 4. Apply Gamification Buff (Hot Streak: -1%)
        print("\n>>> SIMULATION: Applying 'Hot Streak' Buff (-1%)...")
        buffdata = [{"name": "Hot Streak", "reduction": 1.0}]
        breeder.active_buffs = json.dumps(buffdata)
        await session.commit()
        
        fee_3 = await CommissionService.calculate_commission(session, breeder_id)
        print(f"Buffed Fee: {fee_3 * 100}%")
        
        # Expected: 20.0 - 1.0 = 19.0%
        if abs((fee_3 * 100) - 19.0) > 0.01:
             print(f"[FAIL] Buffed Fee Incorrect (Expected 19.0%, Got {fee_3 * 100}%)")
             return
        print("[OK] Gamification Buff Verified.")
        
    print("\n>>> SYSTEM VERIFIED SUCCESSFULLY [OK]")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_commission_system())
