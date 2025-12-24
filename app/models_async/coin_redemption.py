from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import Base

class RedemptionStatus(str, enum.Enum):
    PENDING = "PENDING"
    ESCROW_CREATED = "ESCROW_CREATED"
    COMPLETED = "COMPLETED"
    DISPUTED = "DISPUTED"
    CANCELLED = "CANCELLED"

class CoinRedemption(Base):
    __tablename__ = 'crypto_coin_redemptions'

    id = Column(Integer, primary_key=True, index=True)
    coin_serial = Column(String, unique=True, index=True, nullable=False) # Physical coin QR code content
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True) # User redeeming it
    
    # Optional: Link to an order if the coin was issued for a specific purchase
    # order_id = Column(Integer, ForeignKey('merch_orders.id'), nullable=True) 
    
    status = Column(SQLEnum(RedemptionStatus), default=RedemptionStatus.PENDING)
    
    redeemed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    escrow = relationship("CoinRedemptionEscrow", back_populates="redemption", uselist=False)
    # user = relationship("User") 

class CoinRedemptionEscrow(Base):
    __tablename__ = 'coin_redemption_escrows'

    id = Column(Integer, primary_key=True, index=True)
    redemption_id = Column(Integer, ForeignKey('crypto_coin_redemptions.id'), unique=True, nullable=False)
    
    escrow_address = Column(String, nullable=False) # Algorand Address of the Smart Contract
    app_id = Column(Integer, nullable=False) # Algorand Application ID
    
    amount_held = Column(Float, default=0.0) # Amount in ALGO (or USDC?)
    
    # Status tracking for the on-chain contract
    is_funded = Column(Boolean, default=False)
    is_released = Column(Boolean, default=False)
    is_refunded = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    redemption = relationship("CoinRedemption", back_populates="escrow")
