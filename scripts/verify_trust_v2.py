import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models_async.base import Base
from app.models_async.trust import AuditLog
from app.services.trust_engine.orchestrator_async import AsyncAuditOrchestrator

# Setup In-Memory DB for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async def verify_trust_engine():
    print("🧪 Starting Trust Engine V2 Verification...")
    
    # 1. Setup DB
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SessionLocal() as session:
        orchestrator = AsyncAuditOrchestrator(session)
        
        # 2. Test Audit Request
        print("➡️ Testing process_audit_request...")
        result = await orchestrator.process_audit_request(
            trigger_type="TEST_TRIGGER",
            listing_hash="hash_123",
            merchant_addr="addr_abc",
            strain_name="Blue Dream"
        )
        print(f"⬅️ Result: {result}")
        
        # 3. Verify Persistence
        print("🔎 Verifying AuditLog persistence...")
        log = await session.get(AuditLog, result["log_id"])
        if log:
            print(f"✅ Log Found: ID={log.id}, Status={log.status}, Score={log.trust_score}")
        else:
            print("❌ Log NOT Found!")
            
        # 4. Test Appeal
        print("➡️ Testing process_appeal...")
        appeal_result = await orchestrator.process_appeal(
            listing_id="hash_123",
            reason="It wasn't me!",
            admin_user="admin_dave"
        )
        print(f"⬅️ Appeal Result: {appeal_result}")
        
        appeal_log = await session.get(AuditLog, appeal_result["log_id"])
        if appeal_log and appeal_log.status == "APPROVED_BY_APPEAL":
            print(f"✅ Appeal Log Verified: {appeal_log.raw_data}")
        else:
             print("❌ Appeal Log Failed!")

    print("🏁 Verification Complete.")

if __name__ == "__main__":
    asyncio.run(verify_trust_engine())
