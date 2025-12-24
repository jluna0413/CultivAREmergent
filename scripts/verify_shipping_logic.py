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
from app.models_async.sales import SalesTransaction
from app.models_async.shipping import ShippingStatus
from app.services.shipping_service import ShippingService

# Use in-memory SQLite for testing
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

async def verify_shipping_logic():
    print("\n--- VERIFYING SHIPPING LOGIC (STORY 5) ---\n")
    
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # 1. Setup: User & Transaction
        print(">>> SETUP: Creating Transaction...")
        user = User(username="buyer", email="buyer@test.com", password_hash="pw", is_active=True)
        seller = User(username="seller", email="seller@test.com", password_hash="pw", is_active=True)
        session.add_all([user, seller])
        await session.flush()
        
        tx = SalesTransaction(
            buyer_user_id=user.id,
            seller_user_id=seller.id,
            total_amount=100.0,
            transaction_reference="txn_123"
        )
        session.add(tx)
        await session.commit()
        tx_id = tx.id
        
        # 2. Create Shipment (State: Seed)
        print(f"\n>>> TEST 1: Create Shipment for Tx {tx_id}")
        shipment = await ShippingService.create_shipment(session, tx_id)
        print(f"Status: {shipment.status.value}")
        if shipment.status != ShippingStatus.SEED:
            print(f"[FAIL] Expected Seed, got {shipment.status}")
            return
        print("[OK] Shipment Created (Funds Frozen).")

        # 3. Invalid Transition (Seed -> Harvest)
        print("\n>>> TEST 2: Invalid Transition (Seed -> Harvest)")
        try:
            await ShippingService.update_status(session, shipment.id, "Harvest")
            print("[FAIL] Should have raised ValueError")
            return
        except ValueError as e:
            print(f"[OK] Caught Expected Error: {e}")

        # 4. Valid Lifecycle (Seed -> Seedling -> Vegetative -> Flower -> Harvest)
        print("\n>>> TEST 3: Lifecycle Progression")
        
        # Seedling (Shipped)
        await ShippingService.update_status(session, shipment.id, "Seedling", note="Label Created")
        print(f" -> Transitioned to Seedling")
        
        # Vegetative (Transit)
        await ShippingService.update_status(session, shipment.id, "Vegetative", note="Arrived at Hub")
        print(f" -> Transitioned to Vegetative")
        
        # Flower (Out for Delivery)
        await ShippingService.update_status(session, shipment.id, "Flower", note="On Vehicle")
        print(f" -> Transitioned to Flower")
        
        # Harvest (Delivered)
        print(" -> Transitioning to Harvest (Funds Release)...")
        await ShippingService.update_status(session, shipment.id, "Harvest", note="Delivered at Front Porch")
        
        await session.refresh(shipment)
        if shipment.status != ShippingStatus.HARVEST:
             print(f"[FAIL] Final Status is {shipment.status}")
             return
             
        if "TX_RELEASE" not in (shipment.vault_release_tx or ""):
             print(f"[FAIL] Vault Release TX not recorded: {shipment.vault_release_tx}")
             return
             
        print(f"[OK] Full Lifecycle Complete. Funds Released (Tx: {shipment.vault_release_tx})")
        
    print("\n>>> SYSTEM VERIFIED SUCCESSFULLY [OK]")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_shipping_logic())
