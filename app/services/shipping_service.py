import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models_async.shipping import Shipment, ShippingStatus
from app.models_async.sales import SalesTransaction
# In a real impl, import VaultContract wrapper here

class ShippingService:
    """
    Manages the lifecycle of a shipment:
    Seed -> Seedling -> Vegetative -> Flower -> Harvest.
    Triggers Vault Release on Harvest.
    """

    ALLOWED_TRANSITIONS = {
        ShippingStatus.SEED: [ShippingStatus.SEEDLING, ShippingStatus.CLAWBACK],
        ShippingStatus.SEEDLING: [ShippingStatus.VEGETATIVE, ShippingStatus.CLAWBACK],
        ShippingStatus.VEGETATIVE: [ShippingStatus.FLOWER, ShippingStatus.CLAWBACK],
        ShippingStatus.FLOWER: [ShippingStatus.HARVEST, ShippingStatus.CLAWBACK],
        ShippingStatus.HARVEST: [], # Terminal
        ShippingStatus.CLAWBACK: [] # Terminal
    }

    @staticmethod
    async def create_shipment(db: AsyncSession, transaction_id: int) -> Shipment:
        """Initialize a new shipment in SEED state (Funds Frozen)."""
        # Verify transaction exists
        stmt = select(SalesTransaction).where(SalesTransaction.id == transaction_id)
        result = await db.execute(stmt)
        tx = result.scalar_one_or_none()
        if not tx:
            raise ValueError(f"Transaction {transaction_id} not found.")

        shipment = Shipment(
            transaction_id=transaction_id,
            status=ShippingStatus.SEED,
            tracking_history=json.dumps([{
                "status": "Seed",
                "timestamp": datetime.utcnow().isoformat(),
                "note": "Order Received. Vault Funds Frozen."
            }])
        )
        db.add(shipment)
        await db.commit()
        return shipment

    @staticmethod
    async def update_status(db: AsyncSession, shipment_id: int, new_status: str, note: str = "") -> Shipment:
        """
        Transition shipment status. Triggers Vault Release if HARVEST.
        """
        stmt = select(Shipment).where(Shipment.id == shipment_id)
        result = await db.execute(stmt)
        shipment = result.scalar_one_or_none()
        
        if not shipment:
            raise ValueError(f"Shipment {shipment_id} not found.")

        # Validate Transition
        try:
            target_status = ShippingStatus(new_status)
        except ValueError:
             raise ValueError(f"Invalid Shipping Status: {new_status}")

        if target_status not in ShippingService.ALLOWED_TRANSITIONS.get(shipment.status, []):
             raise ValueError(f"Invalid Transition: {shipment.status} -> {target_status}")

        # Update History
        history = json.loads(shipment.tracking_history)
        history.append({
            "status": target_status.value,
            "timestamp": datetime.utcnow().isoformat(),
            "note": note
        })
        shipment.tracking_history = json.dumps(history)
        shipment.status = target_status
        
        # Trigger Actions
        if target_status == ShippingStatus.SEEDLING:
            # e.g. Notify Buyer
            pass
        elif target_status == ShippingStatus.HARVEST:
            await ShippingService._release_vault_funds(db, shipment)
        elif target_status == ShippingStatus.CLAWBACK:
            await ShippingService._process_refund(db, shipment)

        await db.commit()
        return shipment

    @staticmethod
    async def _release_vault_funds(db: AsyncSession, shipment: Shipment):
        """
        Mock: Call Smart Contract to release funds.
        In production: VaultContract.release(listing_hash)
        """
        print(f"💰 VAULT ALERT: releasing funds for Transaction {shipment.transaction_id} (Status: HARVEST)")
        shipment.vault_release_tx = f"TX_RELEASE_{shipment.transaction_id}_MOCK"

    @staticmethod
    async def _process_refund(db: AsyncSession, shipment: Shipment):
        """
        Mock: Refund Buyer.
        """
        print(f"💸 VAULT ALERT: Refunding Buyer for Transaction {shipment.transaction_id} (Status: CLAWBACK)")
        shipment.vault_release_tx = f"TX_REFUND_{shipment.transaction_id}_MOCK"
