"""
Activities Pydantic Models
Activity request/response models for the FastAPI application.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Activity Models
class ActivityBase(BaseModel):
    """Base activity model."""
    type: str = Field(..., description="Activity type (login, plant_add, strain_edit, etc.)")
    activity_type: str = Field(..., description="Activity category (system, user, plant)")
    title: Optional[str] = Field(None, description="Activity title")
    description: Optional[str] = Field(None, description="Activity description")
    entity_type: Optional[str] = Field(None, description="Entity type (plant, strain, breeder, etc.)")
    entity_id: Optional[int] = Field(None, description="Entity ID")
    entity_name: Optional[str] = Field(None, description="Entity name")
    username: Optional[str] = Field(None, description="Username who performed the activity")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    session_id: Optional[str] = Field(None, description="Session ID")


class ActivityCreate(ActivityBase):
    """Model for creating activities."""
    user_id: Optional[int] = Field(None, description="User ID who performed the activity")
    details: Optional[dict] = Field(None, description="Additional activity details as JSON")
    is_system_activity: bool = Field(False, description="Whether this is a system activity")


class ActivityUpdate(BaseModel):
    """Model for updating activities."""
    title: Optional[str] = Field(None, description="Activity title")
    description: Optional[str] = Field(None, description="Activity description")
    details: Optional[dict] = Field(None, description="Additional activity details as JSON")
    is_active: Optional[bool] = Field(None, description="Whether activity is active")


class ActivityResponse(ActivityBase):
    """Activity response model."""
    id: int = Field(..., description="Activity ID")
    user_id: Optional[int] = Field(None, description="User ID who performed the activity")
    details: Optional[str] = Field(None, description="Additional activity details as JSON string")
    is_system_activity: bool = Field(..., description="Whether this is a system activity")
    is_active: bool = Field(..., description="Whether activity is active")
    timestamp: datetime = Field(..., description="Activity timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    is_recent: bool = Field(..., description="Whether activity is recent (within 24 hours)")

    class Config:
        from_attributes = True


class ActivityListResponse(BaseModel):
    """Paginated activity list response."""
    activities: List[ActivityResponse] = Field(..., description="List of activities")
    total: int = Field(..., description="Total number of activities")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total pages")


# Plant Activity Models
class PlantActivityBase(BaseModel):
    """Base plant activity model."""
    plant_id: int = Field(..., description="Plant ID")
    plant_name: str = Field(..., description="Plant name")
    activity_type: str = Field(..., description="Activity type (feeding, watering, pruning, harvest, etc.)")
    activity_name: str = Field(..., description="Activity name")
    note: Optional[str] = Field(None, description="Activity note")
    username: Optional[str] = Field(None, description="Username who performed the activity")
    ip_address: Optional[str] = Field(None, description="IP address")


class PlantActivityCreate(PlantActivityBase):
    """Model for creating plant activities."""
    user_id: Optional[int] = Field(None, description="User ID who performed the activity")


class PlantActivityUpdate(BaseModel):
    """Model for updating plant activities."""
    activity_name: Optional[str] = Field(None, description="Activity name")
    note: Optional[str] = Field(None, description="Activity note")
    is_active: Optional[bool] = Field(None, description="Whether activity is active")


class PlantActivityResponse(PlantActivityBase):
    """Plant activity response model."""
    id: int = Field(..., description="Activity ID")
    user_id: Optional[int] = Field(None, description="User ID who performed the activity")
    is_active: bool = Field(..., description="Whether activity is active")
    date: datetime = Field(..., description="Activity date")
    created_at: datetime = Field(..., description="Creation timestamp")
    is_recent: bool = Field(..., description="Whether activity is recent (within 7 days)")

    class Config:
        from_attributes = True


class PlantActivityListResponse(BaseModel):
    """Paginated plant activity list response."""
    activities: List[PlantActivityResponse] = Field(..., description="List of plant activities")
    total: int = Field(..., description="Total number of activities")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total pages")


# Activity Summary Models
class ActivityStats(BaseModel):
    """Activity statistics model."""
    total_activities: int = Field(..., description="Total number of activities")
    activities_today: int = Field(..., description="Activities today")
    activities_this_week: int = Field(..., description="Activities this week")
    activities_this_month: int = Field(..., description="Activities this month")
    unique_users: int = Field(..., description="Number of unique users")
    activity_types: List[dict] = Field(..., description="Activity type breakdown")
    recent_activities: int = Field(..., description="Recent activities count")


class ActivitySummaryResponse(BaseModel):
    """Activity summary response model."""
    date: datetime = Field(..., description="Summary date")
    activity_type: str = Field(..., description="Activity type")
    count: int = Field(..., description="Activity count")
    unique_users: int = Field(..., description="Number of unique users")
    entity_type: Optional[str] = Field(None, description="Entity type")
    entity_id: Optional[int] = Field(None, description="Entity ID")

    class Config:
        from_attributes = True


# Activity Filter Models
class ActivityFilters(BaseModel):
    """Activity filtering parameters."""
    type: Optional[str] = Field(None, description="Filter by activity type")
    activity_type: Optional[str] = Field(None, description="Filter by activity category")
    user_id: Optional[int] = Field(None, description="Filter by user ID")
    entity_type: Optional[str] = Field(None, description="Filter by entity type")
    entity_id: Optional[int] = Field(None, description="Filter by entity ID")
    start_date: Optional[datetime] = Field(None, description="Filter by start date")
    end_date: Optional[datetime] = Field(None, description="Filter by end date")
    is_system_activity: Optional[bool] = Field(None, description="Filter by system activity")
    is_active: Optional[bool] = Field(None, description="Filter by active status")


class PlantActivityFilters(BaseModel):
    """Plant activity filtering parameters."""
    plant_id: Optional[int] = Field(None, description="Filter by plant ID")
    activity_type: Optional[str] = Field(None, description="Filter by activity type")
    user_id: Optional[int] = Field(None, description="Filter by user ID")
    start_date: Optional[datetime] = Field(None, description="Filter by start date")
    end_date: Optional[datetime] = Field(None, description="Filter by end date")
    is_active: Optional[bool] = Field(None, description="Filter by active status")


# Utility Models
class ActivityBulkCreate(BaseModel):
    """Model for bulk creating activities."""
    activities: List[ActivityCreate] = Field(..., description="List of activities to create")


class ActivityBulkDelete(BaseModel):
    """Model for bulk deleting activities."""
    activity_ids: List[int] = Field(..., description="List of activity IDs to delete")


class ActivityBulkResponse(BaseModel):
    """Response model for bulk operations."""
    successful: List[int] = Field(..., description="Successfully processed IDs")
    failed: List[int] = Field(..., description="Failed IDs")
    errors: List[str] = Field(..., description="Error messages")


class ActivityTypeResponse(BaseModel):
    """Response model for activity type information."""
    type: str = Field(..., description="Activity type")
    display_name: str = Field(..., description="Display name")
    description: str = Field(..., description="Description")
    category: str = Field(..., description="Category (system, user, plant)")
    is_system: bool = Field(..., description="Whether this is a system activity type")


class ActivityTypeListResponse(BaseModel):
    """Response model for activity type list."""
    types: List[ActivityTypeResponse] = Field(..., description="List of activity types")
    total: int = Field(..., description="Total number of activity types")


# Activity Template Models (for common activity types)
class LoginActivityTemplate(BaseModel):
    """Template for login activities."""
    username: str = Field(..., description="Username")
    success: bool = Field(..., description="Whether login was successful")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")


class PlantActivityTemplate(BaseModel):
    """Template for plant-related activities."""
    plant_id: int = Field(..., description="Plant ID")
    plant_name: str = Field(..., description="Plant name")
    action: str = Field(..., description="Action performed")
    note: Optional[str] = Field(None, description="Additional note")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class SystemActivityTemplate(BaseModel):
    """Template for system activities."""
    action: str = Field(..., description="System action")
    component: str = Field(..., description="System component")
    details: Optional[dict] = Field(None, description="Additional details")
    severity: str = Field("info", description="Severity level (info, warning, error)")