"""
Admin Router
Administrative routes for user and system management.
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.fastapi_app.dependencies import require_admin, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.models_async.auth import User
from app.models_async.grow import Plant, Cultivar

router = APIRouter(prefix="/admin", tags=["admin"])


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


@router.get("/users/{user_id}", name="admin_user_detail")
async def admin_user_detail(
    user_id: int,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin),
    context: dict = Depends(inject_template_context)
):
    """View user details with async SQLAlchemy."""
    try:
        # Fetch user by ID
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get user statistics - plant count
        plant_result = await db.execute(
            select(func.count(Plant.id)).where(Plant.user_id == user_id)
        )
        plant_count = plant_result.scalar() or 0
        
        # Convert user to dict for Jinja2
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at,
        }

        context.update({
            "user": user_dict,
            "plant_count": plant_count,
        })
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error loading user: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    return request.app.state.templates.TemplateResponse(
        "admin/user_detail.html",
        context
    )


@router.post("/api/users/{user_id}/toggle-admin", name="api_admin_toggle_admin")
async def api_toggle_admin(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    """Toggle admin status for a user with async SQLAlchemy."""
    try:
        # Prevent self-modification
        if user_id == current_user.id:
            return {
                "status": "error",
                "message": "Cannot change your own admin status"
            }

        # Fetch user by ID
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Toggle admin status
        user.is_admin = not user.is_admin
        await db.commit()

        return {
            "status": "success",
            "message": f"Admin status {'granted' if user.is_admin else 'revoked'}",
            "is_admin": user.is_admin,
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e),
        }


@router.post("/api/users/{user_id}/delete", name="api_admin_delete_user")
async def api_delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    """Delete a user and their data with async SQLAlchemy."""
    try:
        # Prevent self-deletion
        if user_id == current_user.id:
            return {
                "status": "error",
                "message": "Cannot delete your own account"
            }

        # Fetch user by ID
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete user's plants (cascade delete)
        await db.execute(
            delete(Plant).where(Plant.user_id == user_id)
        )
        
        # Delete user
        await db.delete(user)
        await db.commit()

        return {
            "status": "success",
            "message": "User and associated data deleted"
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e),
        }


@router.get("/api/stats", name="api_admin_stats")
async def api_admin_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    """Get admin statistics."""
    try:
        result = await db.execute(select(func.count(User.id)))
        total_users = result.scalar() or 0
        
        result = await db.execute(select(func.count(Plant.id)))
        total_plants = result.scalar() or 0
        
        result = await db.execute(select(func.count(Cultivar.id)))
        total_cultivars = result.scalar() or 0

        return {
            "status": "success",
            "data": {
                "total_users": total_users,
                "total_plants": total_plants,
                "total_cultivars": total_cultivars,
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


@router.get("/api/users", name="api_admin_all_users")
async def api_admin_all_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_admin)
):
    """Get all users as JSON."""
    try:
        result = await db.execute(
            select(User).order_by(User.created_at.desc())
        )
        users = result.scalars().all()

        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            })

        return {
            "status": "success",
            "data": users_data,
            "total": len(users_data),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


@router.get("/export", name="admin_export")
async def export_page(
    request: Request,
    current_user: User = Depends(require_admin),
    context: dict = Depends(inject_template_context)
):
    """Data export page."""
    context.update({
        "page_title": "Data Export",
        "page_description": "Export your CultivAR data to various formats. Coming soon!"
    })
    return request.app.state.templates.TemplateResponse("views/coming_soon.html", context)


@router.get("/plugins", name="admin_plugins")
async def plugins_page(
    request: Request,
    current_user: User = Depends(require_admin),
    context: dict = Depends(inject_template_context)
):
    """Plugin management page."""
    context.update({
        "page_title": "Plugin Management",
        "page_description": "Manage CultivAR plugins and extensions. Coming soon!"
    })
    return request.app.state.templates.TemplateResponse("views/coming_soon.html", context)
