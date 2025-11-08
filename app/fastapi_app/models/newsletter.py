"""Pydantic models for Newsletter domain."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class NewsletterSubscriberBase(BaseModel):
    """Base newsletter subscriber model."""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    subscription_type: str = Field("both", description="Type of subscription (email, sms, both)")
    source: Optional[str] = Field(None, description="Subscription source")

class NewsletterSubscriberCreate(NewsletterSubscriberBase):
    """Model for creating a new newsletter subscriber."""
    pass

class NewsletterSubscriberResponse(NewsletterSubscriberBase):
    """Model for newsletter subscriber response."""
    id: int
    is_active: bool
    subscription_date: datetime
    unsubscribe_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class NewsletterStats(BaseModel):
    """Model for newsletter statistics."""
    total_subscribers: int
    today_subscriptions: int
    total_unsubscriptions: int
    active_rate: float
