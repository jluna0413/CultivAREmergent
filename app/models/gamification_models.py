"""
Gamification and loyalty system models.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models.base_models import Base


class PointType(enum.Enum):
    """Types of loyalty points"""
    SPROUTS = "sprouts"  # User loyalty points from purchases
    BREEDER_COINS = "breeder_coins"  # Breeder points from coin redemptions


class LoyaltyPointsTransaction(Base):
    """
    Tracks earning and spending of loyalty points.
    """
    __tablename__ = "loyalty_points_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    breeder_id = Column(Integer, ForeignKey("breeders.id"), index=True)
    
    # Point details
    point_type = Column(Enum(PointType), nullable=False)
    amount = Column(Integer, nullable=False)  # Positive for earn, negative for redeem
    balance_after = Column(Integer, nullable=False)
    
    # Transaction details
    transaction_type = Column(String(50), nullable=False)
    # "purchase", "coin_redemption", "merch_redemption", "bonus", "admin_adjustment"
    
    description = Column(Text)
    reference_id = Column(Integer)  # Order ID, coin redemption ID, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    breeder = relationship("Breeder")
    
    def __repr__(self):
        return f"<LoyaltyPointsTransaction(type={self.point_type.value}, amount={self.amount})>"


class UserLoyaltyBalance(Base):
    """
    Current loyalty point balances for users.
    """
    __tablename__ = "user_loyalty_balances"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Balances
    sprouts_balance = Column(Integer, default=0, nullable=False)
    sprouts_lifetime = Column(Integer, default=0, nullable=False)  # Total earned
    
    # Timestamps
    last_earned_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="loyalty_balance")
    
    def __repr__(self):
        return f"<UserLoyaltyBalance(user_id={self.user_id}, sprouts={self.sprouts_balance})>"


class BreederLoyaltyBalance(Base):
    """
    Current loyalty point balances for breeders (coin collection gamification).
    """
    __tablename__ = "breeder_loyalty_balances"
    
    id = Column(Integer, primary_key=True, index=True)
    breeder_id = Column(Integer, ForeignKey("breeders.id"), unique=True, nullable=False)
    
    # Balances
    coin_points_balance = Column(Integer, default=0, nullable=False)
    coin_points_lifetime = Column(Integer, default=0, nullable=False)
    
    # Coin collection stats
    total_coins_redeemed = Column(Integer, default=0)
    bronze_coins = Column(Integer, default=0)
    silver_coins = Column(Integer, default=0)
    gold_coins = Column(Integer, default=0)
    platinum_coins = Column(Integer, default=0)
    
    # Leaderboard rank (updated periodically)
    leaderboard_rank = Column(Integer, index=True)
    
    # Timestamps
    last_earned_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    breeder = relationship("Breeder", back_populates="loyalty_balance")
    
    def __repr__(self):
        return f"<BreederLoyaltyBalance(breeder_id={self.breeder_id}, points={self.coin_points_balance})>"


class MerchCategory(enum.Enum):
    """Merchandise categories"""
    APPAREL = "apparel"
    ACCESSORIES = "accessories"
    GROW_SUPPLIES = "grow_supplies"
    COLLECTIBLES = "collectibles"
    DIGITAL = "digital"


class MerchItem(Base):
    """
    Merchandise redeemable with loyalty points.
    """
    __tablename__ = "merch_items"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Item details
    name = Column(String(150), nullable=False)
    description = Column(Text)
    category = Column(Enum(MerchCategory), nullable=False, index=True)
    image_url = Column(String(255))
    
    # Pricing
    point_cost = Column(Integer, nullable=False, index=True)  # Sprouts or coin points
    point_type = Column(Enum(PointType), nullable=False)  # Which points can redeem
    
    # Inventory
    stock_quantity = Column(Integer, default=0)
    is_available = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False)
    
    # Shipping
    requires_shipping = Column(Boolean, default=True)
    shipping_weight_oz = Column(Float)  # For shipping calculation
    
    # Restrictions
    user_redeemable = Column(Boolean, default=True)  # Can users redeem?
    breeder_only = Column(Boolean, default=False)  # Breeder exclusive?
    admin_only = Column(Boolean, default=False)  # Admin exclusive?
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    redemptions = relationship("MerchRedemption", back_populates="merch_item")
    
    def __repr__(self):
        return f"<MerchItem(id={self.id}, name='{self.name}', cost={self.point_cost})>"


class MerchRedemption(Base):
    """
    Records when users/breeders redeem merch with points.
    """
    __tablename__ = "merch_redemptions"
    
    id = Column(Integer, primary_key=True, index=True)
    merch_item_id = Column(Integer, ForeignKey("merch_items.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    breeder_id = Column(Integer, ForeignKey("breeders.id"), index=True)
    
    # Redemption details
    point_cost = Column(Integer, nullable=False)
    point_type = Column(Enum(PointType), nullable=False)
    quantity = Column(Integer, default=1)
    
    # Shipping (user pays shipping)
    shipping_address_encrypted = Column(LargeBinary)
    shipping_cost = Column(Float)  # User pays this
    shipping_tracking = Column(String(100))
    
    # Status
    status = Column(String(30), default="pending", index=True)
    # "pending", "processing", "shipped", "delivered", "cancelled"
    
    # Timestamps
    redeemed_at = Column(DateTime, default=datetime.utcnow)
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    
    # Relationships
    merch_item = relationship("MerchItem", back_populates="redemptions")
    user = relationship("User")
    breeder = relationship("Breeder")
    
    def __repr__(self):
        return f"<MerchRedemption(id={self.id}, item_id={self.merch_item_id}, status='{self.status}')>"


class BreederLeaderboardEntry(Base):
    """
    Snapshot of breeder leaderboard rankings (updated weekly).
    """
    __tablename__ = "breeder_leaderboard_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    breeder_id = Column(Integer, ForeignKey("breeders.id"), nullable=False)
    
    # Ranking period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Metrics
    rank = Column(Integer, nullable=False, index=True)
    coins_redeemed = Column(Integer, default=0)
    coin_points_earned = Column(Integer, default=0)
    
    # Tier breakdown
    bronze_count = Column(Integer, default=0)
    silver_count = Column(Integer, default=0)
    gold_count = Column(Integer, default=0)
    platinum_count = Column(Integer, default=0)
    
    # Achievements
    achievement_badges = Column(JSON)  # ["first_platinum", "100_coins_club", etc.]
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    breeder = relationship("Breeder")
    
    def __repr__(self):
        return f"<BreederLeaderboardEntry(breeder_id={self.breeder_id}, rank={self.rank})>"
