"""Common Pydantic models for shared functionality."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Common pagination parameters."""
    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel):
    """Common paginated response structure."""
    items: List[dict] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class SearchFilters(BaseModel):
    """Common search and filter parameters."""
    search: Optional[str] = Field(None, description="Search term")
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: Optional[str] = Field("asc", description="Sort order: asc or desc")


class ApiResponse(BaseModel):
    """Standard API response format."""
    status: str = Field(..., description="Response status: success, error")
    message: Optional[str] = Field(None, description="Response message")
    data: Optional[dict] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if status is error")


class HealthCheck(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: Optional[str] = Field(None, description="Application version")
