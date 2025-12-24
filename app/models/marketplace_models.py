"""
Compliance and marketplace operational models.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models.base_models import Base


class StateCannabisLaw(Base):
    """
    State-by-state cannabis seed shipping regulations.
    Updated daily by compliance agent.
    """
    __tablename__ = "state_cannabis_laws"
    
    id = Column(Integer, primary_key=True, index=True)
    state_code = Column(String(2), unique=True, nullable=False, index=True)
    state_name = Column(String(50), nullable=False)
    
    # Legal status
    legal_status = Column(String(20), index=True)  # "legal", "restricted", "illegal"
    seed_shipping_allowed = Column(Boolean, default=False, index=True)
    
    # Details
    restrictions = Column(Text)  # Specific restrictions
    notes = Column(Text)  # Human-readable summary
    source_url = Column(String(255))  # Most recent source
    
    # Tracking
    last_verified = Column(DateTime)
    last_changed = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<StateCannabisLaw(state='{self.state_code}', allowed={self.seed_shipping_allowed})>"


class CoinTier(enum.Enum):
    """Physical crypto coin tiers by value"""
    BRONZE = "bronze"  # $0-50
    SILVER = "silver"  # $50-100
    GOLD = "gold"      # $100-200
    PLATINUM = "platinum"  # $200+


class CryptoCoinRedemption(Base):
    """
    Physical crypto coins issued for restricted states.
    """
    __tablename__ = "crypto_coin_redemptions"
    
    id = Column(Integer, primary_key=True, index=True)
    gnft_pack_id = Column(Integer, ForeignKey("gnft_packs.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    
    # Coin details
    coin_serial = Column(String(20), unique=True, nullable=False, index=True)
    coin_tier = Column(Enum(CoinTier), nullable=False)
    coin_value = Column(Float, nullable=False)  # Matches pack price
    
    # Redemption tracking
    issued_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    issued_address = Column(Text)  # Encrypted shipping address
    issued_at = Column(DateTime)
    
    # Status
    is_redeemed = Column(Boolean, default=False, index=True)
    redeemed_at = Column(DateTime)
    redeemed_by_breeder_id = Column(Integer, ForeignKey("breeders.id"))
    
    # Legal
    restricted_state = Column(String(2), nullable=False)
    reason = Column(Text)  # "State law prohibits seed shipping"
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    pack = relationship("GNFTPack")
    order = relationship("Order", back_populates="coin_redemption")
    user = relationship("User")
    breeder = relationship("Breeder")
    escrow = relationship("CoinRedemptionEscrow", back_populates="coin_redemption", uselist=False)
    
    def __repr__(self):
        return f"<CryptoCoinRedemption(serial='{self.coin_serial}', redeemed={self.is_redeemed})>"


class CoinRedemptionEscrow(Base):
    """
    Algorand smart contract escrows for coin redemptions.
    Payment locked until dual-signature verification.
    """
    __tablename__ = "coin_redemption_escrows"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    coin_redemption_id = Column(Integer, ForeignKey("crypto_coin_redemptions.id"), unique=True)
    
    # Escrow details
    app_id = Column(BigInteger, unique=True)  # Algorand smart contract app ID
    escrow_amount = Column(Float, nullable=False)
    nft_asset_id = Column(BigInteger)
    
    # Parties
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    breeder_id = Column(Integer, ForeignKey("breeders.id"), nullable=False)
    user_address = Column(String(58), nullable=False)  # Algorand address
    breeder_address = Column(String(58), nullable=False)
    
    # Status
    status = Column(String(20), default="locked", index=True)
    # "locked", "released", "refunded"
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # 90 days timeout
    released_at = Column(DateTime)
    release_txn_hash = Column(String(64))
    
    # Relationships
    order = relationship("Order")
    coin_redemption = relationship("CryptoCoinRedemption", back_populates="escrow")
    user = relationship("User")
    breeder = relationship("Breeder")
    
    def __repr__(self):
        return f"<CoinRedemptionEscrow(order_id={self.order_id}, status='{self.status}')>"


class SaleType(enum.Enum):
    """Type of sale transaction"""
    PRIMARY = "primary"      # Initial mint purchase
    SECONDARY = "secondary"  # Resale on marketplace


class SalesTransaction(Base):
    """
    Records all sales with commission tracking.
    """
    __tablename__ = "sales_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    gnft_pack_id = Column(Integer, ForeignKey("gnft_packs.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    
    # Sale details
    sale_type = Column(Enum(SaleType), nullable=False, index=True)
    sale_price = Column(Float, nullable=False)
    
    # Primary sale breakdown
    breeder_revenue = Column(Float)  # 85% of pack price
    platform_commission = Column(Float)  # 15% of pack price
    
    # Secondary sale royalties
    breeder_royalty = Column(Float)  # 7% of resale
    platform_royalty = Column(Float)  # 2% of resale
    minter_royalty = Column(Float)   # 1% of resale
    
    # Fees (primary only)
    minting_fee = Column(Float)  # $2.00 NFT minting
    physical_minting_fee = Column(Float)  # $11.00 for coins
    ipfs_fee = Column(Float)     # $0.50
    shipping_fee = Column(Float) # $5.00 seeds or $3.00 coin
    payment_processing_fee = Column(Float)  # ~3%
    
    # Parties
    seller_user_id = Column(Integer, ForeignKey("users.id"))
    buyer_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    breeder_id = Column(Integer, ForeignKey("breeders.id"), nullable=False)
    
    # Transaction
    payment_txn_hash = Column(String(64))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    pack = relationship("GNFTPack")
    order = relationship("Order", back_populates="sales_transaction", uselist=False)
    seller = relationship("User", foreign_keys=[seller_user_id])
    buyer = relationship("User", foreign_keys=[buyer_user_id])
    breeder = relationship("Breeder")
    royalty_payment = relationship("GNFTRoyaltyPayment", back_populates="sale_transaction", uselist=False)
    
    def __repr__(self):
        return f"<SalesTransaction(id={self.id}, type={self.sale_type.value}, price={self.sale_price})>"


class Order(Base):
    """
    Customer orders for G-NFT purchases.
    """
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("gnft_listings.id"), nullable=False)
    
    # Order details
    pack_size = Column(Integer, nullable=False)
    pack_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Compliance (State only, accessible to agent)
    shipping_state_code = Column(String(2), index=True)
    compliance_checked_at = Column(DateTime)
    fulfillment_method = Column(Enum(FulfillmentMethod))
    restricted_reason = Column(Text)
    
    # Full addresses (ENCRYPTED, NOT accessible to agent)
    shipping_address_encrypted = Column(LargeBinary)
    billing_address_encrypted = Column(LargeBinary)
    
    # Order status
    status = Column(String(30), index=True)
    # "pending_compliance", "pending_breeder_fulfillment", 
    # "pending_coin_fulfillment", "shipped", "delivered", "completed"
    
    # Payment
    payment_method = Column(String(50))  # "stripe", "pera_wallet"
    payment_intent_id = Column(String(100))  # Stripe or Algorand txn
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    listing = relationship("GNFTListing", back_populates="orders")
    coin_redemption = relationship("CryptoCoinRedemption", back_populates="order", uselist=False)
    sales_transaction = relationship("SalesTransaction", back_populates="order", uselist=False)
    
    def __repr__(self):
        return f"<Order(id={self.id}, status='{self.status}')>"
