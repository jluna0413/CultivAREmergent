"""Pydantic models for Blog domain."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    """Base post model with common fields."""
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    slug: str = Field(..., min_length=1, max_length=200, description="URL-friendly slug")
    content: str = Field(..., description="Post content in Markdown")
    author_id: int = Field(..., description="Author's user ID")
    category_id: Optional[int] = Field(None, description="Category ID")
    is_published: bool = Field(False, description="Whether the post is published")
    published_at: Optional[datetime] = Field(None, description="Publication timestamp")
    tags: Optional[List[str]] = Field(None, description="List of tags")

class PostCreate(PostBase):
    """Model for creating a new post."""
    pass

class PostUpdate(BaseModel):
    """Model for updating an existing post."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None
    published_at: Optional[datetime] = None
    tags: Optional[List[str]] = None

class PostResponse(PostBase):
    """Model for post response with computed fields."""
    id: int = Field(..., description="Post ID")
    author_name: str = Field(..., description="Author's name")
    category_name: Optional[str] = Field(None, description="Category name")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    """Model for paginated post list response."""
    items: List[PostResponse] = Field(..., description="List of posts")
    total: int = Field(..., description="Total number of posts")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")
