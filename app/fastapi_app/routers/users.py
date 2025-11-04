"""Users Router - User management with dual-router pattern
HTML template routes + Clean JSON API contracts"""

from fastapi import APIRouter, Request, Depends, HTTPException, status, Query
from sqlalchemy import select, func, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List
import math
from datetime import datetime, timedelta

from app.fastapi_app.dependencies import require_login, inject_template_context, require_admin
from app.models_async.base import get_async_session as get_async_db
from app.fastapi_app.models.users import (
    UserCreate, UserUpdate, UserResponse, UserListResponse,
    UserProfileUpdate, UserPasswordChange, UserStats,
    UserCreateResponse, UserUpdateResponse, UserDeleteResponse,
    UserProfileResponse, UserPasswordResponse, UserFilters
)
from app.fastapi_app.models.common import ApiResponse
from app.models_async.auth import User
from app.models_async.grow import Grow, Plant

# HTML routes for backward compatibility - Legacy template support - DEPRECATED
router = APIRouter(prefix="/users", tags=["users LEGACY - DEPRECATED - Use /api/v1/users"], deprecated=True)

# Clean JSON API routes under /api/v1/users/* - PREFERRED FOR FLUTTER
api_router = APIRouter(prefix="/users", tags=["users-api FLUTTER READY"])


# ============================================================================
# Helper Functions
# ============================================================================

def create_paginated_response(items: List, total: int, page: int, page_size: int) -> dict:
    """Create standardized paginated response."""
    pages = math.ceil(total / page_size) if total > 0 else 0
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1
    }


async def get_user_stats(db: AsyncSession) -> dict:
    """Calculate comprehensive user statistics."""
    try:
        # Total users
        result = await db.execute(select(func.count(User.id)))
        total_users = result.scalar() or 0
        
        # Admin users
        result = await db.execute(select(func.count(User.id)).where(User.is_admin == True))
        admin_users = result.scalar() or 0
        
        # Verified breeders
        result = await db.execute(select(func.count(User.id)).where(User.is_verified_breeder == True))
        verified_breeders = result.scalar() or 0
        
        # Premium users (non-free tier)
        result = await db.execute(select(func.count(User.id)).where(User.tier != 'free'))
        premium_users = result.scalar() or 0
        
        # Active users today
        today = datetime.utcnow().date()
        # Note: This is a placeholder - would need last_login field in User model
        active_users_today = 0
        
        # Active users this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        active_users_week = 0  # Placeholder
        
        # Active users this month
        month_ago = datetime.utcnow() - timedelta(days=30)
        active_users_month = 0  # Placeholder
        
        # New users today
        result = await db.execute(
            select(func.count(User.id)).where(
                func.date(User.created_at) == today
            )
        )
        new_users_today = result.scalar() or 0
        
        # New users this week
        result = await db.execute(
            select(func.count(User.id)).where(
                User.created_at >= week_ago
            )
        )
        new_users_week = result.scalar() or 0
        
        # New users this month
        result = await db.execute(
            select(func.count(User.id)).where(
                User.created_at >= month_ago
            )
        )
        new_users_month = result.scalar() or 0
        
        return {
            "total_users": total_users,
            "admin_users": admin_users,
            "verified_breeders": verified_breeders,
            "premium_users": premium_users,
            "active_users_today": active_users_today,
            "active_users_week": active_users_week,
            "active_users_month": active_users_month,
            "new_users_today": new_users_today,
            "new_users_week": new_users_week,
            "new_users_month": new_users_month
        }
    except Exception as e:
        # Return safe defaults if calculations fail
        return {
            "total_users": 0,
            "admin_users": 0,
            "verified_breeders": 0,
            "premium_users": 0,
            "active_users_today": 0,
            "active_users_week": 0,
            "active_users_month": 0,
            "new_users_today": 0,
            "new_users_week": 0,
            "new_users_month": 0
        }


# ============================================================================
# HTML Pages (Legacy Support)
# ============================================================================

@router.get("/", name="users_list_page")
async def users_list_page(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),  # Admin only
    context: dict = Depends(inject_template_context)
):
    """Display list of users with legacy template support."""
    try:
        # Get users with related data
        result = await db.execute(
            select(User).order_by(User.created_at.desc())
        )
        users = result.scalars().all()
        
        # Transform to match legacy template format
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'is_admin': user.is_admin,
                'user_type': user.user_type,
                'tier': user.tier,
                'is_verified_breeder': user.is_verified_breeder,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            })
        
        context.update({
            "users": user_data,
            "user_count": len(user_data),
        })
        
        return request.app.state.templates.TemplateResponse(
            "admin/users.html",
            context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading users: {str(e)}")


@router.get("/{user_id}", name="user_detail_page")
async def user_detail_page(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),  # Admin only
    context: dict = Depends(inject_template_context)
):
    """Display user detail page."""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's grows and plants count
        grows_count = 0
        plants_count = 0
        
        try:
            result = await db.execute(select(func.count(Grow.id)).where(Grow.user_id == user_id))
            grows_count = result.scalar() or 0
            
            result = await db.execute(select(func.count(Plant.id)).where(Plant.user_id == user_id))
            plants_count = result.scalar() or 0
        except Exception:
            # Ignore errors if relationships don't exist
            pass
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'is_admin': user.is_admin,
            'user_type': user.user_type,
            'tier': user.tier,
            'is_verified_breeder': user.is_verified_breeder,
            'force_password_change': user.force_password_change,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'grows_count': grows_count,
            'plants_count': plants_count
        }
        
        context.update({
            "user": user_data,
        })
        
        return request.app.state.templates.TemplateResponse(
            "admin/user.html",
            context
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading user: {str(e)}")


@router.get("/profile", name="current_user_profile_page")
async def current_user_profile_page(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Display current user's profile page."""
    try:
        # Get user's grows and plants count
        grows_count = 0
        plants_count = 0
        
        try:
            result = await db.execute(select(func.count(Grow.id)).where(Grow.user_id == current_user.id))
            grows_count = result.scalar() or 0
            
            result = await db.execute(select(func.count(Plant.id)).where(Plant.user_id == current_user.id))
            plants_count = result.scalar() or 0
        except Exception:
            # Ignore errors if relationships don't exist
            pass
        
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'phone': current_user.phone,
            'is_admin': current_user.is_admin,
            'user_type': current_user.user_type,
            'tier': current_user.tier,
            'is_verified_breeder': current_user.is_verified_breeder,
            'force_password_change': current_user.force_password_change,
            'created_at': current_user.created_at,
            'updated_at': current_user.updated_at,
            'grows_count': grows_count,
            'plants_count': plants_count
        }
        
        context.update({
            "user": user_data,
        })
        
        return request.app.state.templates.TemplateResponse(
            "profile.html",
            context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading profile: {str(e)}")


# ============================================================================
# Clean JSON API Contracts
# ============================================================================

@api_router.get("/list", name="api_users_list")
async def api_users_list(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),  # Admin only
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    user_type: Optional[str] = Query(None, description="Filter by user type"),
    tier: Optional[str] = Query(None, description="Filter by user tier"),
    is_admin: Optional[bool] = Query(None, description="Filter by admin status"),
):
    """Get paginated list of users with filters - Clean JSON API."""
    try:
        # Build base query
        query = select(User)
        
        # Apply filters
        if search:
            query = query.where(
                or_(
                    User.username.contains(search),
                    User.email.contains(search)
                )
            )
        
        if user_type:
            query = query.where(User.user_type == user_type)
        
        if tier:
            query = query.where(User.tier == tier)
        
        if is_admin is not None:
            query = query.where(User.is_admin == is_admin)
        
        # Get total count
        count_query = select(func.count(User.id))
        # Apply same filters for count
        if search:
            count_query = count_query.where(
                or_(
                    User.username.contains(search),
                    User.email.contains(search)
                )
            )
        if user_type:
            count_query = count_query.where(User.user_type == user_type)
        if tier:
            count_query = count_query.where(User.tier == tier)
        if is_admin is not None:
            count_query = count_query.where(User.is_admin == is_admin)
        
        result = await db.execute(count_query)
        total = result.scalar() or 0
        
        # Apply pagination and ordering
        query = query.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        
        # Execute main query
        result = await db.execute(query)
        users = result.scalars().all()
        
        # Transform to response format
        items = []
        for user in users:
            items.append(UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                phone=user.phone,
                user_type=user.user_type,
                tier=user.tier,
                is_verified_breeder=user.is_verified_breeder,
                is_admin=user.is_admin,
                force_password_change=user.force_password_change,
                created_at=user.created_at,
                updated_at=user.updated_at,
                has_grows=None,  # Could be populated with eager loading
                grows_count=None,  # Could be populated with separate query
                plants_count=None,  # Could be populated with separate query
                last_login=None  # Would need last_login field in User model
            ))
        
        return UserListResponse(**create_paginated_response(items, total, page, page_size))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")


@api_router.get("/{user_id}", name="api_user_get")
async def api_user_get(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),  # Admin only
):
    """Get user details - Clean JSON API."""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            user_type=user.user_type,
            tier=user.tier,
            is_verified_breeder=user.is_verified_breeder,
            is_admin=user.is_admin,
            force_password_change=user.force_password_change,
            created_at=user.created_at,
            updated_at=user.updated_at,
            has_grows=None,
            grows_count=None,
            plants_count=None,
            last_login=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


@api_router.post("/", name="api_user_create")
async def api_user_create(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),  # Admin only
):
    """Create a new user - Clean JSON API."""
    try:
        # Check if username already exists
        result = await db.execute(select(User).where(User.username == user_data.username))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Check if email already exists (if provided)
        if user_data.email:
            result = await db.execute(select(User).where(User.email == user_data.email))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="Email already exists")
        
        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            phone=user_data.phone,
            user_type=user_data.user_type,
            tier=user_data.tier,
            is_verified_breeder=user_data.is_verified_breeder,
            is_admin=user_data.is_admin
        )
        user.set_password(user_data.password)
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return UserCreateResponse(
            message="User created successfully",
            status="created",
            user_id=user.id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


@api_router.patch("/{user_id}", name="api_user_update")
async def api_user_update(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),  # Admin only
):
    """Update an existing user - Clean JSON API."""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check username uniqueness if being updated
        if user_data.username and user_data.username != user.username:
            result = await db.execute(select(User).where(User.username == user_data.username))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="Username already exists")
        
        # Check email uniqueness if being updated
        if user_data.email and user_data.email != user.email:
            result = await db.execute(select(User).where(User.email == user_data.email))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="Email already exists")
        
        # Update fields
        update_data = user_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        await db.commit()
        
        return UserUpdateResponse(
            message="User updated successfully",
            status="updated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")


@api_router.delete("/{user_id}", name="api_user_delete")
async def api_user_delete(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),  # Admin only
):
    """Delete a user - Clean JSON API."""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prevent deleting yourself
        if user.id == current_user.id:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
        await db.delete(user)
        await db.commit()
        
        return UserDeleteResponse(
            message="User deleted successfully",
            status="deleted"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")


@api_router.get("/me", name="api_current_user_profile")
async def api_current_user_profile(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get current user profile - Clean JSON API."""
    try:
        return UserProfileResponse(
            message="Profile retrieved successfully",
            user=UserResponse(
                id=current_user.id,
                username=current_user.username,
                email=current_user.email,
                phone=current_user.phone,
                user_type=current_user.user_type,
                tier=current_user.tier,
                is_verified_breeder=current_user.is_verified_breeder,
                is_admin=current_user.is_admin,
                force_password_change=current_user.force_password_change,
                created_at=current_user.created_at,
                updated_at=current_user.updated_at,
                has_grows=None,
                grows_count=None,
                plants_count=None,
                last_login=None
            )
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {str(e)}")


@api_router.patch("/me", name="api_update_own_profile")
async def api_update_own_profile(
    profile_data: UserProfileUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Update current user profile - Clean JSON API."""
    try:
        # Check username uniqueness if being updated
        if profile_data.username and profile_data.username != current_user.username:
            result = await db.execute(select(User).where(User.username == profile_data.username))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="Username already exists")
        
        # Check email uniqueness if being updated
        if profile_data.email and profile_data.email != current_user.email:
            result = await db.execute(select(User).where(User.email == profile_data.email))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="Email already exists")
        
        # Update fields
        update_data = profile_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(current_user, key, value)
        
        await db.commit()
        
        return UserUpdateResponse(
            message="Profile updated successfully",
            status="updated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating profile: {str(e)}")


@api_router.patch("/me/password", name="api_change_password")
async def api_change_password(
    password_data: UserPasswordChange,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Change current user password - Clean JSON API."""
    try:
        # Verify current password
        if not current_user.check_password(password_data.current_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        # Set new password
        current_user.set_password(password_data.new_password)
        current_user.force_password_change = False
        
        await db.commit()
        
        return UserPasswordResponse(
            message="Password changed successfully",
            status="updated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error changing password: {str(e)}")


@api_router.get("/stats", name="api_user_stats")
async def api_user_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),  # Admin only
):
    """Get user statistics - Clean JSON API."""
    try:
        stats = await get_user_stats(db)
        return UserStats(**stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user stats: {str(e)}")


# Note: This router needs to be included in the main FastAPI app with both routers
# In __init__.py: app.include_router(users.router, tags=["Users Legacy"])
#                app.include_router(users.api_router, prefix="/api/v1", tags=["Users API"])