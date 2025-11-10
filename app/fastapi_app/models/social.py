"""Pydantic models for Social domain."""
from pydantic import BaseModel, Field
from typing import Optional, Dict

class ShareRequest(BaseModel):
    platform: str
    url: str
    title: Optional[str] = None
    description: Optional[str] = None

class ShareStats(BaseModel):
    total_shares: int
    platform_breakdown: Dict[str, int]
    top_posts: list
