"""
Async Authentication Models
User model without Flask-Login dependencies.
"""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, Integer, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.models_async.base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.models_async.grow import Grow, Plant


class User(Base):
    """User model for authentication (pure async)."""
    
    __tablename__ = "user"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Required Fields
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    
    # Optional Fields
    email: Mapped[Optional[str]] = mapped_column(String(120), unique=True, nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # User Type and Permissions
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_type: Mapped[str] = mapped_column(String(50), default='Grower', nullable=False)
    tier: Mapped[str] = mapped_column(String(50), default='free', nullable=False)
    is_verified_breeder: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    force_password_change: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships (lazy loaded)
    grows: Mapped[List["Grow"]] = relationship("Grow", back_populates="user", lazy="selectin")
    plants: Mapped[List["Plant"]] = relationship("Plant", back_populates="user", lazy="selectin")
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author", lazy="selectin")
    
    def __init__(
        self,
        username: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        is_admin: bool = False,
        force_password_change: bool = False,
        **kwargs
    ):
        """
        Initialize user (password must be set via set_password method).
        
        Args:
            username: Unique username
            email: User email (optional)
            phone: User phone (optional)
            is_admin: Admin flag
            force_password_change: Force password change on next login
            **kwargs: Additional fields
            
        Raises:
            ValueError: If password-related kwargs are provided
        """
        # Prevent direct password setting
        password_related_keys = {'password', 'password_hash', 'passwd', 'pwd'}
        for key in password_related_keys:
            if key in kwargs:
                raise ValueError(f"Cannot set '{key}' through constructor. Use set_password() method instead.")
        
        # Call parent init
        super().__init__(**kwargs)
        
        # Set fields
        self.username = username
        self.email = email
        self.phone = phone
        self.is_admin = is_admin
        self.force_password_change = force_password_change
    
    def set_password(self, password: str) -> None:
        """
        Hash and set user password.
        
        Args:
            password: Plain text password
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """
        Verify password against stored hash.
        
        Args:
            password: Plain text password to check
            
        Returns:
            True if password matches, False otherwise
        """
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    async def has_grows(self, session: "AsyncSession") -> bool:
        """
        Check if user has any grows.
        
        Args:
            session: Async database session
            
        Returns:
            True if user has grows, False otherwise
        """
        from app.models_async.grow import Grow
        
        result = await session.execute(
            select(func.count()).select_from(Grow).where(Grow.user_id == self.id)
        )
        count = result.scalar_one()
        return count > 0
    
    async def get_active_grows(self, session: "AsyncSession") -> List["Grow"]:
        """
        Get all active grows for this user.
        
        Args:
            session: Async database session
            
        Returns:
            List of active Grow instances
        """
        from app.models_async.grow import Grow
        
        result = await session.execute(
            select(Grow).where(Grow.user_id == self.id, Grow.status == 'active')
        )
        return list(result.scalars().all())
    
    async def get_plants(self, session: "AsyncSession") -> List["Plant"]:
        """
        Get all plants for this user.
        
        Args:
            session: Async database session
            
        Returns:
            List of Plant instances
        """
        from app.models_async.grow import Plant
        
        result = await session.execute(
            select(Plant).where(Plant.user_id == self.id)
        )
        return list(result.scalars().all())
    
    def to_dict(self) -> dict:
        """
        Convert user to dictionary (excludes password_hash).
        
        Returns:
            Dictionary representation of user
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "is_admin": self.is_admin,
            "user_type": self.user_type,
            "tier": self.tier,
            "is_verified_breeder": self.is_verified_breeder,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', is_admin={self.is_admin})>"
