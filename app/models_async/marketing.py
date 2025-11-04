"""
Async Marketing Models
Waitlist, Newsletter, Blog, LeadMagnet models.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models_async.base import Base


class Waitlist(Base):
    """Waitlist model for pre-launch signups."""
    
    __tablename__ = "waitlist"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    
    # User Information
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    experience: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # beginner, intermediate, advanced, expert
    
    # Priority and Referral
    priority_tier: Mapped[str] = mapped_column(String(20), default='general', nullable=False)
    referral_code: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    referral_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # How they heard about us
    referred_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('waitlist.id'), nullable=True)
    
    # Status
    is_activated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Tracking
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    signup_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Waitlist(id={self.id}, email='{self.email}', name='{self.name}')>"


class NewsletterSubscriber(Base):
    """Newsletter subscriber model (email and/or phone)."""
    
    __tablename__ = "newsletter_subscriber"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(120), unique=True, nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True, index=True)
    
    # Subscription Settings
    subscription_type: Mapped[str] = mapped_column(String(20), default='both', nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Metadata
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    preferences: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    
    # Dates
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    unsubscribe_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    @property
    def is_unsubscribed(self) -> bool:
        """Check if user is unsubscribed."""
        return self.unsubscribe_date is not None
    
    def __repr__(self) -> str:
        return f"<NewsletterSubscriber(id={self.id}, email='{self.email}')>"


class BlogPost(Base):
    """Blog post model for content marketing."""
    
    __tablename__ = "blog_post"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Details
    excerpt: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    author: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # SEO
    meta_description: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    featured_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Status
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Dates
    publish_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    @property
    def tags_list(self) -> list:
        """Return tags as a list."""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []
    
    @property
    def reading_time(self) -> int:
        """Estimate reading time in minutes."""
        if not self.content:
            return 0
        words_per_minute = 200
        word_count = len(self.content.split())
        return max(1, round(word_count / words_per_minute))
    
    def __repr__(self) -> str:
        return f"<BlogPost(id={self.id}, slug='{self.slug}')>"


class LeadMagnet(Base):
    """Lead magnet model for tracking downloadable resources."""
    
    __tablename__ = "lead_magnet"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    download_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    downloads: Mapped[list["LeadMagnetDownload"]] = relationship("LeadMagnetDownload", back_populates="lead_magnet", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<LeadMagnet(id={self.id}, name='{self.name}')>"


class LeadMagnetDownload(Base):
    """Track individual lead magnet downloads."""
    
    __tablename__ = "lead_magnet_download"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_magnet_id: Mapped[int] = mapped_column(Integer, ForeignKey('lead_magnet.id', ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    
    # Tracking
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Timestamp
    download_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    lead_magnet = relationship("LeadMagnet", back_populates="downloads")
    
    def __repr__(self) -> str:
        return f"<LeadMagnetDownload(id={self.id}, lead_magnet_id={self.lead_magnet_id}, email='{self.email}')>"
