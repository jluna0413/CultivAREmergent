"""Pydantic models for Users domain."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator, EmailStr


class UserBase(BaseModel):
    """Base user model with common fields."""
    username: str = Field(..., min_length=3, max_length=80, description="Unique username")
    email: Optional[EmailStr] = Field(None, description="User email address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    user_type: str = Field("Grower", description="User type (Grower, Breeder, Admin, etc.)")
    tier: str = Field("free", description="User tier (free, premium, pro)")
    is_verified_breeder: bool = Field(False, description="Whether user is verified breeder")


class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., min_length=8, description="User password")
    is_admin: bool = Field(False, description="Admin privileges flag")


class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    username: Optional[str] = Field(None, min_length=3, max_length=80)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    user_type: Optional[str] = None
    tier: Optional[str] = None
    is_verified_breeder: Optional[bool] = None
    is_admin: Optional[bool] = None
    force_password_change: Optional[bool] = None


class UserResponse(UserBase):
    """Model for user response with computed fields."""
    id: int = Field(..., description="User ID")
    is_admin: bool = Field(..., description="Admin privileges flag")
    force_password_change: bool = Field(..., description="Force password change flag")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    # Computed fields
    has_grows: Optional[bool] = Field(None, description="Whether user has grows")
    grows_count: Optional[int] = Field(None, description="Number of grows")
    plants_count: Optional[int] = Field(None, description="Number of plants")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Model for paginated user list response."""
    items: List[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class UserProfileUpdate(BaseModel):
    """Model for user profile updates."""
    username: Optional[str] = Field(None, min_length=3, max_length=80)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)


class UserPasswordChange(BaseModel):
    """Model for password change."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")


class UserStats(BaseModel):
    """Model for user statistics."""
    total_users: int = Field(..., description="Total number of users")
    admin_users: int = Field(..., description="Number of admin users")
    verified_breeders: int = Field(..., description="Number of verified breeders")
    premium_users: int = Field(..., description="Number of premium users")
    active_users_today: int = Field(..., description="Users active today")
    active_users_week: int = Field(..., description="Users active this week")
    active_users_month: int = Field(..., description="Users active this month")
    new_users_today: int = Field(..., description="New users today")
    new_users_week: int = Field(..., description="New users this week")
    new_users_month: int = Field(..., description="New users this month")


class UserCreateResponse(BaseModel):
    """Response model for user creation API."""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")
    user_id: int = Field(..., description="Created user ID")


class UserUpdateResponse(BaseModel):
    """Response model for user update API."""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


class UserDeleteResponse(BaseModel):
    """Response model for user deletion API."""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


class UserProfileResponse(BaseModel):
    """Response model for user profile API."""
    message: str = Field(..., description="Response message")
    user: UserResponse = Field(..., description="User profile data")


class UserPasswordResponse(BaseModel):
    """Response model for password change API."""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


class UserFilters(BaseModel):
    """Model for user filtering parameters."""
    search: Optional[str] = Field(None, description="Search term for username/email")
    user_type: Optional[str] = Field(None, description="Filter by user type")
    tier: Optional[str] = Field(None, description="Filter by user tier")
    is_admin: Optional[bool] = Field(None, description="Filter by admin status")
    is_verified_breeder: Optional[bool] = Field(None, description="Filter by breeder verification")
    created_after: Optional[datetime] = Field(None, description="Filter users created after date")
    created_before: Optional[datetime] = Field(None, description="Filter users created before date")