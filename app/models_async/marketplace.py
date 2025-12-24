"""
Marketplace Models

Database models for the marketplace including:
- Auctions (foundation for future auction house)
- Listings
- Bids

Part of the marketplace foundation for reduced future refactoring.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, 
    Text, ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
import enum

from .base import Base


class AuctionStatus(enum.Enum):
    """Auction status types"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    ENDING_SOON = "ending_soon"
    ENDED = "ended"
    SOLD = "sold"
    CANCELLED = "cancelled"
    NO_SALE = "no_sale"


class ListingType(enum.Enum):
    """Marketplace listing types"""
    FIXED_PRICE = "fixed_price"
    AUCTION = "auction"
    AUCTION_WITH_BUY_NOW = "auction_with_buy_now"


class SellerType(enum.Enum):
    """Seller types for marketplace"""
    HOUSE = "house"  # CultivAR official
    VERIFIED_BREEDER = "verified_breeder"  # Future: verified breeders
    COMMUNITY = "community"  # Future: community sellers


class MarketplaceListing(Base):
    """
    Marketplace listing for genetics.
    Supports both fixed price and auction formats.
    """
    __tablename__ = "marketplace_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Seller info
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    seller_type = Column(SQLEnum(SellerType), default=SellerType.HOUSE, nullable=False)
    
    # Listing details
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    listing_type = Column(SQLEnum(ListingType), default=ListingType.FIXED_PRICE, nullable=False)
    
    # Product info
    strain_name = Column(String(100), nullable=False)
    breeder_name = Column(String(100), nullable=True)
    seed_count = Column(Integer, default=1)
    seed_type = Column(String(50), nullable=True)  # regular, feminized, autoflower
    
    # Pricing (for fixed price listings)
    price = Column(Float, nullable=True)
    
    # NFT info (optional)
    nft_asset_id = Column(String(100), nullable=True)  # Algorand ASA ID
    nft_required = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    quantity_available = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    seller = relationship("User", back_populates="marketplace_listings")
    auction = relationship("Auction", back_populates="listing", uselist=False)
    
    def __repr__(self):
        return f"<MarketplaceListing(id={self.id}, title={self.title}, type={self.listing_type})>"


class Auction(Base):
    """
    Auction model for the auction house.
    
    Phase 1: Only CultivAR (house) can create auctions
    Phase 2: Verified breeders can create auctions
    """
    __tablename__ = "auctions"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("marketplace_listings.id"), nullable=False, unique=True)
    
    # Auction parameters
    starting_price = Column(Float, nullable=False)
    reserve_price = Column(Float, nullable=True)  # Minimum price to sell
    buy_now_price = Column(Float, nullable=True)  # Optional instant purchase price
    bid_increment = Column(Float, default=1.00)  # Minimum bid increase
    
    # Current state
    current_bid = Column(Float, nullable=True)
    current_bidder_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    bid_count = Column(Integer, default=0)
    
    # Timing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    extended_end_time = Column(DateTime, nullable=True)  # Anti-sniping extension
    
    # Status
    status = Column(SQLEnum(AuctionStatus), default=AuctionStatus.DRAFT, nullable=False)
    
    # Winner info
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    final_price = Column(Float, nullable=True)
    
    # Settings
    allow_extensions = Column(Boolean, default=True)  # Anti-sniping
    extension_minutes = Column(Integer, default=5)  # Add time if bid in last X minutes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    listing = relationship("MarketplaceListing", back_populates="auction")
    current_bidder = relationship("User", foreign_keys=[current_bidder_id])
    winner = relationship("User", foreign_keys=[winner_id])
    bids = relationship("AuctionBid", back_populates="auction", order_by="AuctionBid.created_at.desc()")
    
    @property
    def is_active(self) -> bool:
        now = datetime.utcnow()
        return self.status == AuctionStatus.ACTIVE and self.start_time <= now <= self.end_time
    
    @property
    def time_remaining_seconds(self) -> int:
        if not self.is_active:
            return 0
        end = self.extended_end_time or self.end_time
        return max(0, int((end - datetime.utcnow()).total_seconds()))
    
    def __repr__(self):
        return f"<Auction(id={self.id}, status={self.status}, current_bid={self.current_bid})>"


class AuctionBid(Base):
    """
    Individual bid on an auction.
    """
    __tablename__ = "auction_bids"
    
    id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False, index=True)
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Bid details
    amount = Column(Float, nullable=False)
    is_winning = Column(Boolean, default=False)
    is_auto_bid = Column(Boolean, default=False)  # From max bid feature
    
    # Metadata
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    auction = relationship("Auction", back_populates="bids")
    bidder = relationship("User")
    
    def __repr__(self):
        return f"<AuctionBid(id={self.id}, auction_id={self.auction_id}, amount={self.amount})>"


class AuctionWatch(Base):
    """
    Users watching auctions for notifications.
    """
    __tablename__ = "auction_watches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False, index=True)
    
    # Notification preferences
    notify_outbid = Column(Boolean, default=True)
    notify_ending = Column(Boolean, default=True)
    notify_ended = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User")
    auction = relationship("Auction")
