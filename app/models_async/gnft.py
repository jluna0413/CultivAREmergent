"""
G-NFT (Genetics NFT) models for fractional genetics marketplace.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, BigInteger, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models_async.base import Base


class PackSize(enum.Enum):
    """Standard pack sizes"""
    THREE = 3
    FIVE = 5
    SIX = 6
    TEN = 10
    TWELVE = 12


class FulfillmentMethod(enum.Enum):
    """How order is fulfilled"""
    BREEDER_SHIPS_SEEDS = "breeder_ships_seeds"
    PLATFORM_SHIPS_COIN = "platform_ships_coin"


class ExclusiveDropNFT(Base):
    """
    Exclusive Drop NFT representing entire seed harvest.
    Created by breeders for their harvests.
    Previously known as Master Harvest NFT.
    """
    __tablename__ = "exclusive_drop_nfts"
    
    id = Column(Integer, primary_key=True, index=True)
    breeder_id = Column(Integer, ForeignKey("marketplace_breeders.id"), nullable=False)
    genetics_id = Column(Integer, ForeignKey("user_genetics.id"), nullable=False)
    
    # Blockchain
    master_asset_id = Column(BigInteger, unique=True, index=True)  # Algorand ASA ID (Master Asset)
    ipfs_metadata_hash = Column(String(64))  # IPFS CID
    
    # Harvest details
    harvest_name = Column(String(100), nullable=False)  # e.g., "Blue Dream F5 2024 Spring Harvest"
    total_seed_count = Column(Integer, nullable=False)  # Original harvest size
    seeds_remaining = Column(Integer, nullable=False)  # Not yet packed
    seeds_packed = Column(Integer, default=0)  # Allocated to packs
    seeds_burned = Column(Integer, default=0)  # Packs burned
    
    # Scarcity tracking
    scarcity_score = Column(Float, default=0.0, index=True)  # 0-100
    last_scarcity_update = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    minted_at = Column(DateTime)
    
    # Relationships
    breeder = relationship("MarketplaceBreeder", back_populates="exclusive_drops")
    genetics = relationship("UserGenetics")
    packs = relationship("GNFTPack", back_populates="exclusive_drop", cascade="all, delete-orphan")
    listings = relationship("GNFTListing", back_populates="exclusive_drop")
    
    def __repr__(self):
        return f"<ExclusiveDropNFT(id={self.id}, name='{self.harvest_name}', seeds={self.total_seed_count})>"


class GNFTPack(Base):
    """
    Fractional pack G-NFT derived from Exclusive Drop NFT.
    Tradeable, burnable unit (3, 5, 6, 10, or 12 seeds).
    """
    __tablename__ = "gnft_packs"
    
    id = Column(Integer, primary_key=True, index=True)
    exclusive_drop_id = Column(Integer, ForeignKey("exclusive_drop_nfts.id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("gnft_listings.id"))
    
    # Blockchain
    pack_asset_id = Column(BigInteger, unique=True, index=True)  # Algorand ASA ID
    ipfs_metadata_hash = Column(String(64))
    
    # Pack details
    pack_size = Column(Integer, nullable=False)  # 3, 5, 6, 10, or 12
    pack_number = Column(Integer, nullable=False)  # Sequential within master
    
    # Ownership
    current_owner_id = Column(Integer, ForeignKey("users.id"))
    first_minter_user_id = Column(Integer, ForeignKey("users.id"))  # For 10% royalty
    
    # Burn status
    is_burned = Column(Boolean, default=False, index=True)
    burned_at = Column(DateTime)
    burned_for_grow_id = Column(Integer, ForeignKey("grows.id"))
    
    # Pricing history
    mint_price = Column(Float)  # Original purchase price
    last_sale_price = Column(Float)
    floor_price = Column(Float)  # Lowest current listing
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    minted_at = Column(DateTime)
    
    # Relationships
    exclusive_drop = relationship("ExclusiveDropNFT", back_populates="packs")
    listing = relationship("GNFTListing", back_populates="packs")
    current_owner = relationship("User", foreign_keys=[current_owner_id])
    first_minter = relationship("User", foreign_keys=[first_minter_user_id])
    burn_history = relationship("GNFTBurnHistory", back_populates="pack", uselist=False)
    
    def __repr__(self):
        return f"<GNFTPack(id={self.id}, size={self.pack_size}, burned={self.is_burned})>"


class GNFTListing(Base):
    """
    Pre-mint marketplace listing created by breeder.
    Lazy minting: NFTs created when user purchases.
    """
    __tablename__ = "gnft_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    breeder_id = Column(Integer, ForeignKey("marketplace_breeders.id"), nullable=False)
    exclusive_drop_id = Column(Integer, ForeignKey("exclusive_drop_nfts.id"))  # Null until drop minted
    genetics_id = Column(Integer, ForeignKey("user_genetics.id"), nullable=False)
    
    # Listing details
    listing_title = Column(String(150), nullable=False)
    description = Column(Text)
    total_seeds_available = Column(Integer, nullable=False)
    seeds_sold = Column(Integer, default=0)
    
    # Pack availability & pricing (breeder sets prices per pack size)
    pack_3_price = Column(Float)
    pack_3_available = Column(Integer, default=0)
    
    pack_5_price = Column(Float)
    pack_5_available = Column(Integer, default=0)
    
    pack_6_price = Column(Float)
    pack_6_available = Column(Integer, default=0)
    
    pack_10_price = Column(Float)
    pack_10_available = Column(Integer, default=0)
    
    pack_12_price = Column(Float)
    pack_12_available = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    breeder = relationship("MarketplaceBreeder", back_populates="listings")
    exclusive_drop = relationship("ExclusiveDropNFT", back_populates="listings")
    genetics = relationship("UserGenetics")
    packs = relationship("GNFTPack", back_populates="listing")
    # orders = relationship("Order", back_populates="listing")
    
    def __repr__(self):
        return f"<GNFTListing(id={self.id}, title='{self.listing_title}')>"


class GNFTBurnHistory(Base):
    """
    Records when packs are burned (used in grows).
    """
    __tablename__ = "gnft_burn_history"
    
    id = Column(Integer, primary_key=True, index=True)
    pack_id = Column(Integer, ForeignKey("gnft_packs.id"), unique=True, nullable=False)
    exclusive_drop_id = Column(Integer, ForeignKey("exclusive_drop_nfts.id"), nullable=False)
    
    # Burn details
    burned_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    grow_id = Column(Integer, ForeignKey("grows.id"))
    burn_txn_hash = Column(String(64))  # Algorand transaction hash
    
    # Scarcity impact
    scarcity_before = Column(Float)
    scarcity_after = Column(Float)
    
    # Timestamp
    burned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    pack = relationship("GNFTPack", back_populates="burn_history")
    exclusive_drop = relationship("ExclusiveDropNFT")
    user = relationship("User")
    grow = relationship("Grow")
    
    def __repr__(self):
        return f"<GNFTBurnHistory(pack_id={self.pack_id}, burned_at={self.burned_at})>"


class GNFTRoyaltyConfig(Base):
    """
    Royalty configuration for Exclusive Drop NFT.
    Default: 70% breeder, 20% platform, 10% first minter.
    """
    __tablename__ = "gnft_royalty_config"
    
    id = Column(Integer, primary_key=True, index=True)
    exclusive_drop_id = Column(Integer, ForeignKey("exclusive_drop_nfts.id"), unique=True, nullable=False)
    
    # Royalty percentages (in basis points, e.g., 7000 = 70%)
    total_royalty_bps = Column(Integer, default=1000)  # 10% total royalty
    breeder_share_bps = Column(Integer, default=7000)  # 70% of royalty
    platform_share_bps = Column(Integer, default=2000)  # 20% of royalty
    first_minter_share_bps = Column(Integer, default=1000)  # 10% of royalty
    
    # ARC-69 royalty address
    royalty_address = Column(String(58))  # Smart contract address
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    exclusive_drop = relationship("ExclusiveDropNFT")
    
    def __repr__(self):
        return f"<GNFTRoyaltyConfig(exclusive_drop_id={self.exclusive_drop_id})>"


class GNFTRoyaltyPayment(Base):
    """
    Records royalty distributions from secondary sales.
    """
    __tablename__ = "gnft_royalty_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    pack_id = Column(Integer, ForeignKey("gnft_packs.id"), nullable=False)
    sale_transaction_id = Column(Integer, ForeignKey("sales_transactions.id"))
    
    # Sale details
    sale_price = Column(Float, nullable=False)
    total_royalty_amount = Column(Float, nullable=False)
    
    # Distribution (all in cents or microalgos)
    breeder_amount = Column(Float, nullable=False)
    platform_amount = Column(Float, nullable=False)
    first_minter_amount = Column(Float, nullable=False)
    
    # Payment tracking
    breeder_paid_at = Column(DateTime)
    first_minter_paid_at = Column(DateTime)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    pack = relationship("GNFTPack")
    sale_transaction = relationship("SalesTransaction")
    
    def __repr__(self):
        return f"<GNFTRoyaltyPayment(pack_id={self.pack_id}, total={self.total_royalty_amount})>"
