"""
Activities Router - Activity tracking and management
Dual-router pattern: HTML template routes + Clean JSON API contracts
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status, Query
from sqlalchemy import select, func, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List
import math
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.fastapi_app.models.activities import (
    ActivityCreate, ActivityUpdate, ActivityResponse, ActivityListResponse,
    PlantActivityCreate, PlantActivityUpdate, PlantActivityResponse, PlantActivityListResponse,
    ActivityFilters, PlantActivityFilters, ActivityStats, ActivityTypeResponse, ActivityTypeListResponse,
    ActivityBulkCreate, ActivityBulkResponse, LoginActivityTemplate, PlantActivityTemplate, SystemActivityTemplate
)
from app.fastapi_app.models.common import ApiResponse
from app.models_async.auth import User
from app.models_async.activities import Activity, PlantActivity, ActivitySummary
from app.models_async.grow import Plant

# HTML routes for backward compatibility - Legacy template support
router = APIRouter(tags=["activities"])

# Clean JSON API routes under /api/v1/activities/*
api_router = APIRouter(tags=["activities-api"])


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


def get_activity_types() -> List[ActivityTypeResponse]:
    """Get predefined activity types."""
    return [
        ActivityTypeResponse(
            type="login",
            display_name="User Login",
            description="User login events",
            category="user",
            is_system=False
        ),
        ActivityTypeResponse(
            type="logout",
            display_name="User Logout",
            description="User logout events",
            category="user",
            is_system=False
        ),
        ActivityTypeResponse(
            type="plant_add",
            display_name="Plant Added",
            description="Plant creation activities",
            category="plant",
            is_system=False
        ),
        ActivityTypeResponse(
            type="plant_edit",
            display_name="Plant Updated",
            description="Plant update activities",
            category="plant",
            is_system=False
        ),
        ActivityTypeResponse(
            type="plant_delete",
            display_name="Plant Deleted",
            description="Plant deletion activities",
            category="plant",
            is_system=False
        ),
        ActivityTypeResponse(
            type="cultivar_add",
            display_name="Cultivar Added",
            description="Cultivar creation activities",
            category="system",
            is_system=True
        ),
        ActivityTypeResponse(
            type="cultivar_edit",
            display_name="Cultivar Updated",
            description="Cultivar update activities",
            category="system",
            is_system=True
        ),
        ActivityTypeResponse(
            type="cultivar_deleted",
            display_name="Cultivar Deleted",
            description="Cultivar deletion activities",
            category="system",
            is_system=True
        ),
        # Legacy cultivar types for backward compatibility
        ActivityTypeResponse(
            type="cultivar_add",
            display_name="Cultivar Added (Legacy)",
            description="Legacy cultivar creation activities - use cultivar_add instead",
            category="system",
            is_system=True
        ),
        ActivityTypeResponse(
            type="cultivar_edit",
            display_name="Cultivar Updated (Legacy)",
            description="Legacy cultivar update activities - use cultivar_edit instead",
            category="system",
            is_system=True
        ),
        ActivityTypeResponse(
            type="user_add",
            display_name="User Added",
            description="User creation activities",
            category="system",
            is_system=True
        ),
        ActivityTypeResponse(
            type="system_error",
            display_name="System Error",
            description="System error events",
            category="system",
            is_system=True
        ),
        ActivityTypeResponse(
            type="sensor_reading",
            display_name="Sensor Reading",
            description="Sensor data events",
            category="system",
            is_system=True
        ),
    ]


# ============================================================================
# HTML Pages (Legacy Support)
# ============================================================================

@router.get("/", name="activities_list_page")
async def activities_list_page(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Display list of activities with legacy template support."""
    try:
        # Get recent activities with eager loading
        result = await db.execute(
            select(Activity).order_by(Activity.timestamp.desc()).limit(50)
        )
        activities = result.scalars().all()
        
        # Transform to match legacy template format
        activity_data = []
        for activity in activities:
            activity_data.append({
                'id': activity.id,
                'type': activity.type,
                'activity_type': activity.activity_type,
                'title': activity.title,
                'description': activity.description,
                'username': activity.username,
                'entity_type': activity.entity_type,
                'entity_name': activity.entity_name,
                'timestamp': activity.timestamp.isoformat() if activity.timestamp else None,
                'is_system_activity': activity.is_system_activity,
                'is_recent': activity.is_recent
            })
        
        context.update({
            "activities": activity_data,
            "activity_count": len(activity_data),
        })
        
        return request.app.state.templates.TemplateResponse(
            "views/activities.html",
            context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading activities: {str(e)}")


# ============================================================================
# Clean JSON API Contracts
# ============================================================================

class ActivityListApiResponse(BaseModel):
    """Response model for activity list API."""
    activities: List[ActivityResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool


class ActivityCreateResponse(BaseModel):
    """Response model for activity creation API."""
    message: str
    status: str
    activity_id: int


class ActivityUpdateResponse(BaseModel):
    """Response model for activity update API."""
    message: str
    status: str


class ActivityDeleteResponse(BaseModel):
    """Response model for activity deletion API."""
    message: str
    status: str


@api_router.get("/list", response_model=ActivityListApiResponse, name="api_activities_list")
async def api_activities_list(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    type: Optional[str] = Query(None, description="Filter by type"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    entity_type: Optional[str] = Query(None, description="Filter by entity type"),
    entity_id: Optional[int] = Query(None, description="Filter by entity ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    is_system_activity: Optional[bool] = Query(None, description="Filter by system activity"),
):
    """Get paginated list of activities with filters - Clean JSON API."""
    try:
        # Build base query
        query = select(Activity).options(selectinload(Activity.user))
        
        # Apply filters
        if activity_type:
            query = query.where(Activity.activity_type == activity_type)
        
        if type:
            query = query.where(Activity.type == type)
        
        if user_id:
            query = query.where(Activity.user_id == user_id)
        
        if entity_type:
            query = query.where(Activity.entity_type == entity_type)
        
        if entity_id:
            query = query.where(Activity.entity_id == entity_id)
        
        if is_system_activity is not None:
            query = query.where(Activity.is_system_activity == is_system_activity)
        
        if start_date:
            query = query.where(Activity.timestamp >= start_date)
        
        if end_date:
            query = query.where(Activity.timestamp <= end_date)
        
        # Get total count
        count_query = select(func.count(Activity.id))
        # Apply same filters for count
        if activity_type:
            count_query = count_query.where(Activity.activity_type == activity_type)
        if type:
            count_query = count_query.where(Activity.type == type)
        if user_id:
            count_query = count_query.where(Activity.user_id == user_id)
        if entity_type:
            count_query = count_query.where(Activity.entity_type == entity_type)
        if entity_id:
            count_query = count_query.where(Activity.entity_id == entity_id)
        if is_system_activity is not None:
            count_query = count_query.where(Activity.is_system_activity == is_system_activity)
        if start_date:
            count_query = count_query.where(Activity.timestamp >= start_date)
        if end_date:
            count_query = count_query.where(Activity.timestamp <= end_date)
        
        result = await db.execute(count_query)
        total = result.scalar() or 0
        
        # Apply pagination and ordering
        query = query.order_by(Activity.timestamp.desc()).offset((page - 1) * page_size).limit(page_size)
        
        # Execute main query
        result = await db.execute(query)
        activities = result.scalars().all()
        
        # Transform to response format
        items = []
        for activity in activities:
            items.append(ActivityResponse(
                id=activity.id,
                type=activity.type,
                activity_type=activity.activity_type,
                user_id=activity.user_id,
                username=activity.user.username if activity.user else activity.username,
                entity_type=activity.entity_type,
                entity_id=activity.entity_id,
                entity_name=activity.entity_name,
                title=activity.title,
                description=activity.description,
                details=activity.details,
                ip_address=activity.ip_address,
                user_agent=activity.user_agent,
                session_id=activity.session_id,
                is_system_activity=activity.is_system_activity,
                is_active=activity.is_active,
                timestamp=activity.timestamp,
                created_at=activity.created_at,
                updated_at=activity.updated_at,
                is_recent=activity.is_recent
            ))
        
        return ActivityListApiResponse(**create_paginated_response(items, total, page, page_size))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching activities: {str(e)}")


@api_router.get("/{activity_id}", response_model=ActivityResponse, name="api_activity_get")
async def api_activity_get(
    activity_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get activity details - Clean JSON API."""
    try:
        result = await db.execute(select(Activity).where(Activity.id == activity_id).options(selectinload(Activity.user)))
        activity = result.scalar_one_or_none()
        
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        return ActivityResponse(
            id=activity.id,
            type=activity.type,
            activity_type=activity.activity_type,
            user_id=activity.user_id,
            username=activity.user.username if activity.user else activity.username,
            entity_type=activity.entity_type,
            entity_id=activity.entity_id,
            entity_name=activity.entity_name,
            title=activity.title,
            description=activity.description,
            details=activity.details,
            ip_address=activity.ip_address,
            user_agent=activity.user_agent,
            session_id=activity.session_id,
            is_system_activity=activity.is_system_activity,
            is_active=activity.is_active,
            timestamp=activity.timestamp,
            created_at=activity.created_at,
            updated_at=activity.updated_at,
            is_recent=activity.is_recent
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching activity: {str(e)}")


@api_router.post("/", response_model=ActivityCreateResponse, name="api_activity_create")
async def api_activity_create(
    activity_data: ActivityCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Create a new activity - Clean JSON API."""
    try:
        # Create activity
        activity = Activity(
            type=activity_data.type,
            activity_type=activity_data.activity_type,
            user_id=activity_data.user_id or current_user.id,
            username=activity_data.username,
            entity_type=activity_data.entity_type,
            entity_id=activity_data.entity_id,
            entity_name=activity_data.entity_name,
            title=activity_data.title,
            description=activity_data.description,
            details=activity_data.details,
            ip_address=activity_data.ip_address,
            user_agent=activity_data.user_agent,
            session_id=activity_data.session_id,
            is_system_activity=activity_data.is_system_activity
        )
        
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        
        return ActivityCreateResponse(
            message="Activity created successfully",
            status="created",
            activity_id=activity.id
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating activity: {str(e)}")


@api_router.patch("/{activity_id}", response_model=ActivityUpdateResponse, name="api_activity_update")
async def api_activity_update(
    activity_id: int,
    activity_data: ActivityUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Update an existing activity - Clean JSON API."""
    try:
        result = await db.execute(select(Activity).where(Activity.id == activity_id))
        activity = result.scalar_one_or_none()
        
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        # Update fields
        update_data = activity_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(activity, key, value)
        
        await db.commit()
        
        return ActivityUpdateResponse(
            message="Activity updated successfully",
            status="updated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating activity: {str(e)}")


@api_router.delete("/{activity_id}", response_model=ActivityDeleteResponse, name="api_activity_delete")
async def api_activity_delete(
    activity_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Delete an activity - Clean JSON API."""
    try:
        result = await db.execute(select(Activity).where(Activity.id == activity_id))
        activity = result.scalar_one_or_none()
        
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        await db.delete(activity)
        await db.commit()
        
        return ActivityDeleteResponse(
            message="Activity deleted successfully",
            status="deleted"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting activity: {str(e)}")


@api_router.get("/stats", response_model=ActivityStats, name="api_activities_stats")
async def api_activities_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get activity statistics - Clean JSON API."""
    try:
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=7)
        month_start = today_start.replace(day=1)
        
        # Total activities
        result = await db.execute(select(func.count(Activity.id)))
        total_activities = result.scalar() or 0
        
        # Activities today
        result = await db.execute(
            select(func.count(Activity.id)).where(Activity.timestamp >= today_start)
        )
        activities_today = result.scalar() or 0
        
        # Activities this week
        result = await db.execute(
            select(func.count(Activity.id)).where(Activity.timestamp >= week_start)
        )
        activities_this_week = result.scalar() or 0
        
        # Activities this month
        result = await db.execute(
            select(func.count(Activity.id)).where(Activity.timestamp >= month_start)
        )
        activities_this_month = result.scalar() or 0
        
        # Unique users
        result = await db.execute(
            select(func.count(func.distinct(Activity.user_id))).where(Activity.user_id.isnot(None))
        )
        unique_users = result.scalar() or 0
        
        # Activity types breakdown
        result = await db.execute(
            select(Activity.type, func.count(Activity.id))
            .group_by(Activity.type)
            .order_by(func.count(Activity.id).desc())
        )
        activity_types = [{"type": row[0], "count": row[1]} for row in result.all()]
        
        # Recent activities (last 24 hours)
        recent_cutoff = now - timedelta(hours=24)
        result = await db.execute(
            select(func.count(Activity.id)).where(Activity.timestamp >= recent_cutoff)
        )
        recent_activities = result.scalar() or 0
        
        return ActivityStats(
            total_activities=total_activities,
            activities_today=activities_today,
            activities_this_week=activities_this_week,
            activities_this_month=activities_this_month,
            unique_users=unique_users,
            activity_types=activity_types,
            recent_activities=recent_activities
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching activity stats: {str(e)}")


@api_router.get("/types", response_model=ActivityTypeListResponse, name="api_activity_types")
async def api_activity_types(
    current_user: User = Depends(require_login),
):
    """Get available activity types - Clean JSON API."""
    try:
        types = get_activity_types()
        return ActivityTypeListResponse(
            types=types,
            total=len(types)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching activity types: {str(e)}")


# ============================================================================
# Convenience endpoints for common activity types
# ============================================================================

@api_router.post("/login", response_model=ActivityCreateResponse, name="api_activity_login")
async def api_record_login(
    login_data: LoginActivityTemplate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Record a login activity."""
    try:
        activity = Activity(
            type="login",
            activity_type="user",
            user_id=current_user.id,
            username=current_user.username,
            title="User Login",
            description=f"User {login_data.username} {'successful' if login_data.success else 'failed'} login",
            ip_address=login_data.ip_address,
            user_agent=login_data.user_agent,
            session_id=request.session.get("session_id") if hasattr(request, 'session') else None,
            is_system_activity=False
        )
        
        # Add success/failure details
        activity.set_details({
            "success": login_data.success,
            "username": login_data.username,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        
        return ActivityCreateResponse(
            message="Login activity recorded successfully",
            status="created",
            activity_id=activity.id
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error recording login activity: {str(e)}")


@api_router.post("/plant-activity", response_model=ActivityCreateResponse, name="api_activity_plant")
async def api_record_plant_activity(
    plant_data: PlantActivityTemplate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Record a plant activity."""
    try:
        activity = Activity(
            type="plant_activity",
            activity_type="plant",
            user_id=current_user.id,
            username=current_user.username,
            entity_type="plant",
            entity_id=plant_data.plant_id,
            entity_name=plant_data.plant_name,
            title=f"Plant Activity: {plant_data.action}",
            description=f"Activity '{plant_data.action}' performed on plant {plant_data.plant_name}",
            ip_address=request.client.host if request.client else None,
            is_system_activity=False
        )
        
        # Add plant-specific details
        activity.set_details({
            "action": plant_data.action,
            "note": plant_data.note,
            "metadata": plant_data.metadata
        })
        
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        
        return ActivityCreateResponse(
            message="Plant activity recorded successfully",
            status="created",
            activity_id=activity.id
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error recording plant activity: {str(e)}")


@api_router.post("/system-activity", response_model=ActivityCreateResponse, name="api_activity_system")
async def api_record_system_activity(
    system_data: SystemActivityTemplate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
):
    """Record a system activity."""
    try:
        activity = Activity(
            type="system_activity",
            activity_type="system",
            title=f"System: {system_data.action}",
            description=f"System action '{system_data.action}' on {system_data.component}",
            is_system_activity=True
        )
        
        # Add system-specific details
        activity.set_details({
            "action": system_data.action,
            "component": system_data.component,
            "details": system_data.details,
            "severity": system_data.severity
        })
        
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        
        return ActivityCreateResponse(
            message="System activity recorded successfully",
            status="created",
            activity_id=activity.id
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error recording system activity: {str(e)}")


# Note: This router needs to be included in the main FastAPI app with both routers
# In __init__.py: app.include_router(activities.router, tags=["Activities Legacy"])
#                app.include_router(activities.api_router, prefix="/api/v1", tags=["Activities API"])