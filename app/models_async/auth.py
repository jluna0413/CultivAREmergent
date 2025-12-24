"""
Asynchronous database models for CultivAR application.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
)
from .base import Base
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.validators import validate_password



from sqlalchemy.orm import relationship

class User(Base):
    """Asynchronous User model for authentication."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    phone = Column(String(20))
    email = Column(String(120))
    force_password_change = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_type = Column(String(50), default='user')
    tier = Column(String(50), default='free') # Added
    is_verified_breeder = Column(Boolean, default=False) # Added

    activity_logs = relationship("ActivityLog", back_populates="user")
    plant_activities = relationship("PlantActivity", back_populates="user")
    plants = relationship("Plant", back_populates="user")
    blog_posts = relationship("BlogPost", back_populates="author_rel")
    
    # Gamification relationships
    xp_record = relationship("UserXP", back_populates="user", uselist=False, cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    streak_record = relationship("UserStreak", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Marketplace relationships
    marketplace_listings = relationship("MarketplaceListing", back_populates="seller", cascade="all, delete-orphan")
    breeder = relationship("MarketplaceBreeder", back_populates="user", uselist=False)
    wallets = relationship("UserWallet", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, username=None, phone=None, email=None, password_hash=None, is_admin=False, is_active=True, force_password_change=False, user_type='user', tier='free', is_verified_breeder=False, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.phone = phone
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.is_active = is_active
        self.force_password_change = force_password_change
        self.user_type = user_type
        self.tier = tier
        self.is_verified_breeder = is_verified_breeder

    def set_password(self, password):
        """Hashes the password and sets the password_hash."""
        is_valid, error = validate_password(password)
        if not is_valid:
            raise ValueError(error)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
