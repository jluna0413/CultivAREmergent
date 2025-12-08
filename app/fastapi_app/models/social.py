"""Pydantic models for Social domain."""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict

class ShareRequest(BaseModel):
    platform: str
    url: str
    title: Optional[str] = None
    description: Optional[str] = None

    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must be a valid URL (e.g., http://example.com)')
        return v

class ShareStats(BaseModel):
    total_shares: int
    platform_breakdown: Dict[str, int]
    top_posts: list
