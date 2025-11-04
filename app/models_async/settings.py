"""
Async Settings Models
Application settings and extensions.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models_async.base import Base


class Settings(Base):
    """Application settings model (key-value store)."""
    
    __tablename__ = "settings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<Settings(key='{self.key}', value='{self.value}')>"


class Extension(Base):
    """Extension/plugin model for marketplace."""
    
    __tablename__ = "extension"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Version
    version: Mapped[str] = mapped_column(String(20), default='1.0.0', nullable=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_installed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Metadata
    author: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Timestamps
    installed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<Extension(id={self.id}, name='{self.name}', version='{self.version}')>"
