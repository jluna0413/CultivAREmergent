"""Pydantic models for Marketing domain."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

class WaitlistEntryBase(BaseModel):
    """Base waitlist entry model."""
    email: EmailStr
    priority_tier: str = Field("general", description="Priority tier for the waitlist")
    referral_code: Optional[str] = None

class WaitlistEntryCreate(WaitlistEntryBase):
    """Model for creating a new waitlist entry."""
    pass

class WaitlistEntryResponse(WaitlistEntryBase):
    """Model for waitlist entry response."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WaitlistStats(BaseModel):
    """Model for waitlist statistics."""
    total: int
    today: int
    this_week: int

class LeadMagnetBase(BaseModel):
    """Base lead magnet model."""
    name: str
    file_path: str
    download_count: int = 0

class LeadMagnetCreate(LeadMagnetBase):
    """Model for creating a new lead magnet."""
    pass

class LeadMagnetResponse(LeadMagnetBase):
    """Model for lead magnet response."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
