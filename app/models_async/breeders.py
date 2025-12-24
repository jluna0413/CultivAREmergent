"""
Breeder models for genetics marketplace.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models_async.base import Base


class MarketplaceBreeder(Base):
    """
    Verified breeders who can list G-NFTs on marketplace
    """
    __tablename__ = "marketplace_breeders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    breeder_id = Column(Integer, ForeignKey("breeders.id"), nullable=True) # Link to global breeder record
    
    # Profile
    breeder_name = Column(String(100), unique=True, nullable=False, index=True)
    bio = Column(Text)
    website_url = Column(String(255))
    logo_url = Column(String(255))
    
    # Verification
    is_verified = Column(Boolean, default=False, index=True)
    verified_at = Column(DateTime)
    verification_notes = Column(Text)
    
    # Blockchain
    algorand_address = Column(String(58), unique=True)  # Algorand wallet
    
    # Payment
    payment_address = Column(String(255))  # For fiat payouts
    payment_method = Column(String(50))  # "bank_transfer", "stripe", etc.
    
    # Stats
    total_sales = Column(Integer, default=0)
    total_revenue = Column(Integer, default=0)  # in cents
    rating_avg = Column(Integer, default=0)  # 0-5000 (5.0 stars)
    rating_count = Column(Integer, default=0)
    
    today_sales = Column(Integer, default=0) # Reset daily via cron
    month_sales = Column(Integer, default=0) # Reset monthly via cron
    month_reset_date = Column(DateTime, default=datetime.utcnow)
    
    # Gamification
    current_tier = Column(String(50), default="Starter") # Starter, Mover, Shaker, Market Maker
    active_buffs = Column(Text, default="[]") # JSON list of active buffs
    fee_override = Column(Integer, nullable=True) # Custom fee in basis points (e.g. 1000 = 10%)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="breeder")
    listings = relationship("GNFTListing", back_populates="breeder", cascade="all, delete-orphan")
    exclusive_drops = relationship("ExclusiveDropNFT", back_populates="breeder", cascade="all, delete-orphan")
    global_breeder = relationship("Breeder", back_populates="marketplace_profile")
    
    def __repr__(self):
        return f"<MarketplaceBreeder(id={self.id}, name='{self.breeder_name}', verified={self.is_verified})>"
