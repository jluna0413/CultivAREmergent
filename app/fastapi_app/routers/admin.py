"""
Admin Router
Administrative routes for user and system management.
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import List

from app.fastapi_app.dependencies import require_admin, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.models_async.auth import User
from app.models_async.grow import Plant, Cultivar
from app.fastapi_app.models.admin import AdminStats, AdminUserBulkDeleteRequest, SystemInfo, LogEntry
from app.fastapi_app.models.users import UserResponse

# HTML routes for backward compatibility - Legacy template support
router = APIRouter(tags=["admin"])

# Clean JSON API routes under /api/v1/admin/*
api_router = APIRouter(tags=["admin-api"])


@router.get("/", name="admin_home")
async def admin_home(request: Request):
    """Redirect to admin dashboard."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=request.url_for("admin_dashboard"))


@router.get("/dashboard", name="admin_dashboard")
async def admin_dashboard(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),
    context: dict = Depends(inject_template_context)
):
    """Admin dashboard with system statistics."""
    try:
        # System statistics
        result = await db.execute(select(func.count(User.id)))
        total_users = result.scalar() or 0
        
        result = await db.execute(
            select(func.count(User.id)).where(User.is_admin == True)
        )
        admin_users = result.scalar() or 0
        
        result = await db.execute(select(func.count(Plant.id)))
        total_plants = result.scalar() or 0
        
        result = await db.execute(select(func.count(Cultivar.id)))
        total_cultivars = result.scalar() or 0
        
        # Activity in last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        result = await db.execute(
            select(func.count(func.distinct(Plant.user_id))).where(
                Plant.start_dt >= thirty_days_ago
            )
        )
        active_users_30d = result.scalar() or 0

        context.update({
            "total_users": total_users,
            "admin_users": admin_users,
            "total_plants": total_plants,
            "total_cultivars": total_cultivars,
            "active_users_30d": active_users_30d,
        })
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")

    return request.app.state.templates.TemplateResponse(
        "admin/dashboard.html",
        context
    )

@router.get("/users", name="admin_users")
async def admin_users(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),
    context: dict = Depends(inject_template_context)
):
    """User management page with async SQLAlchemy."""
    try:
        # Fetch all users ordered by creation date
        result = await db.execute(
            select(User).order_by(User.created_at.desc())
        )
        users = result.scalars().all()
        
        # Calculate statistics
        total_users = len(users)
        admin_count = sum(1 for u in users if u.is_admin)
        
        # Convert users to dicts for Jinja2 compatibility
        users_data = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "is_admin": u.is_admin,
                "created_at": u.created_at,
            }
            for u in users
        ]
        
        context.update({
            "users": users_data,
            "total_users": total_users,
            "admin_count": admin_count,
        })
    except Exception as e:
        print(f"Error loading users: {e}")
        context.update({
            "users": [],
            "total_users": 0,
            "admin_count": 0,
        })
    
    return request.app.state.templates.TemplateResponse(
        "admin/users_clean.html",
        context
    )

# API Routes

@api_router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    """Get admin statistics."""
    result = await db.execute(select(func.count(User.id)))
    total_users = result.scalar() or 0
    
    result = await db.execute(select(func.count(Plant.id)))
    total_plants = result.scalar() or 0
    
    result = await db.execute(select(func.count(Cultivar.id)))
    total_cultivars = result.scalar() or 0

    return AdminStats(
        total_users=total_users,
        total_plants=total_plants,
        total_cultivars=total_cultivars,
        total_breeders=0, # Placeholder
        total_clones=0, # Placeholder
        total_activities=0, # Placeholder
        total_sensors=0 # Placeholder
    )

@api_router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    """Get all users as JSON."""
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [UserResponse.from_orm(user) for user in users]

@api_router.post("/users/bulk-delete")
async def bulk_delete_users(
    request: AdminUserBulkDeleteRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    if current_user.id in request.user_ids:
        raise HTTPException(status_code=400, detail="Cannot delete your own account.")
    
    await db.execute(delete(User).where(User.id.in_(request.user_ids)))
    await db.commit()
    return {"status": "success", "message": "Users deleted."}

@api_router.post("/users/{user_id}/toggle-admin")
async def toggle_admin(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot change your own admin status.")
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user.is_admin = not user.is_admin
    await db.commit()
    return {"status": "success", "is_admin": user.is_admin}

@api_router.post("/users/{user_id}/force-password-reset")
async def force_password_reset(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user.force_password_change = True
    await db.commit()
    return {"status": "success", "message": "User will be required to reset password on next login."}

@api_router.get("/system/info", response_model=SystemInfo)
async def get_system_info():
    # This is placeholder data. A real implementation would gather this dynamically.
    return SystemInfo(
        python_version="3.9",
        os_name="Linux",
        os_version="Ubuntu 20.04",
        cpu_count="8",
        memory_total="16 GB",
        memory_available="8 GB",
        disk_total="512 GB",
        disk_free="256 GB",
        boot_time=str(datetime.utcnow() - timedelta(days=1))
    )

@api_router.get("/system/logs", response_model=List[LogEntry])
async def get_system_logs():
    # This is placeholder data. A real implementation would read from a log file.
    return [
        LogEntry(timestamp=str(datetime.utcnow()), level="INFO", message="System started"),
        LogEntry(timestamp=str(datetime.utcnow() - timedelta(minutes=5)), level="WARNING", message="High CPU usage detected"),
    ]
