"""
Shipping models for the Marketplace Order Lifecycle.
Lifecycle: Bean -> Sprout -> Vegetative -> Flower -> Harvest.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models_async.base import Base

class ShippingStatus(enum.Enum):
    SEED = "Seed"             # Order Received / Funds Frozen (Was Bean)
    SEEDLING = "Seedling"     # Shipped / Label Created (Was Sprout)
    VEGETATIVE = "Vegetative" # In Transit
    FLOWER = "Flower"         # Out for Delivery
    HARVEST = "Harvest"       # Delivered / Funds Released
    CLAWBACK = "Clawback"     # Refunded due to failure

class Shipment(Base):
    """
    Tracks the physical delivery of a SalesTransaction.
    """
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("sales_transactions.id"), nullable=False, unique=True)
    
    status = Column(Enum(ShippingStatus), default=ShippingStatus.SEED)
    
    tracking_number = Column(String(255), nullable=True)
    carrier = Column(String(100), nullable=True) # USPS, UPS, FedEx
    estimated_delivery = Column(DateTime, nullable=True)
    
    # Vault / Blockchain integration
    vault_release_tx = Column(String(255), nullable=True) # Algorand TxID of 90% release
    
    # Metadata for tracking updates
    tracking_history = Column(Text, default="[]") # JSON list of events
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transaction = relationship("SalesTransaction", backref="shipment")
