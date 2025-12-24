"""
Sales Transaction models for marketplace.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models_async.base import Base

class TransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class SalesTransaction(Base):
    """
    Records a financial transaction for a sale.
    """
    __tablename__ = "sales_transactions"

    id = Column(Integer, primary_key=True, index=True)
    buyer_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    total_amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    
    payment_method = Column(String(50)) # e.g. "stripe", "crypto"
    transaction_reference = Column(String(255)) # Stripe ID or Tx Hash
    
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    buyer = relationship("User", foreign_keys=[buyer_user_id])
    seller = relationship("User", foreign_keys=[seller_user_id])
    # items = relationship("OrderItem", ...) # Can be added later
