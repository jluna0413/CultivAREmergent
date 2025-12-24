"""
Asynchronous database models for marketing-related data.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    func,
    JSON # Import JSON type
)
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

class NewsletterSubscriber(Base):
    """Asynchronous Newsletter Subscriber model."""
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    phone = Column(String(20), unique=True)
    subscription_type = Column(String(20), default='both')
    is_active = Column(Boolean, default=True)
    subscription_date = Column(DateTime, default=func.now())
    unsubscribe_date = Column(DateTime)
    ip_address = Column(String(45))
    preferences = Column(Text)
    source = Column(String(50))

    @property
    def contact_info(self):
        if self.email:
            return self.email
        elif self.phone:
            return self.phone
        return None

    @property
    def is_unsubscribed(self):
        return self.unsubscribe_date is not None


class Waitlist(Base):
    """Asynchronous Waitlist model for pre-launch signups."""
    __tablename__ = "waitlist"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(100))
    experience = Column(String(100))
    phone = Column(String(20))
    referral_source = Column(String(100))
    priority_tier = Column(String(20), default='general')
    referral_code = Column(String(20), unique=True)
    referred_by = Column(Integer, ForeignKey('waitlist.id'))
    signup_date = Column(DateTime, default=func.now())
    is_activated = Column(Boolean, default=False)
    ip_address = Column(String(45))
    user_agent = Column(String(255))

    referrer = relationship("Waitlist", remote_side=[id], back_populates="referred_users")
    referred_users = relationship("Waitlist", back_populates="referrer")

    # referral_count would require an async query, so it's better implemented as a handler function.

    @property
    def signup_date_formatted(self):
        return self.signup_date.strftime('%B %d, %Y') if self.signup_date else None


class BlogPost(Base):
    """Asynchronous Blog post model for content marketing."""
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(String(300)) # Added
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Changed from author (String)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    featured_image = Column(String(255)) # Added
    meta_description = Column(String(160)) # Added
    tags = Column(JSON) # Changed from String to JSON
    view_count = Column(Integer, default=0) # Added
    categories = Column(JSON) # Changed from Text to JSON
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    author_rel = relationship("User", back_populates="blog_posts") # New relationship

    @property
    def publish_date_formatted(self):
        return self.published_at.strftime('%B %d, %Y') if self.published_at else None

    @property
    def reading_time(self):
        if not self.content:
            return 0
        words_per_minute = 200
        word_count = len(self.content.split())
        return max(1, round(word_count / words_per_minute))

    @property
    def tags_list(self):
        return self.tags if self.tags else [] # Updated for JSON type


class LeadMagnet(Base):
    """Asynchronous Lead magnet model for tracking downloads."""
    __tablename__ = "lead_magnets"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    file_path = Column(String(255), nullable=False)
    download_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    downloads = relationship("LeadMagnetDownload", back_populates="lead_magnet")


class LeadMagnetDownload(Base):
    """Asynchronous model to track individual lead magnet downloads."""
    __tablename__ = "lead_magnet_downloads"

    id = Column(Integer, primary_key=True)
    lead_magnet_id = Column(Integer, ForeignKey('lead_magnets.id'), nullable=False)
    email = Column(String(120), nullable=False)
    ip_address = Column(String(45))
    download_date = Column(DateTime, default=func.now())
    user_agent = Column(String(255))

    lead_magnet = relationship('LeadMagnet', back_populates='downloads')


# Alias for backward compatibility
WaitlistEntry = Waitlist