"""
Async user management handlers for the CultivAR application.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.logger import logger
from app.models_async.auth import User
from app.handlers_async import activity_handlers

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_all_users_async(session: AsyncSession):
    """
    Get all users with their details and activity summary.
    """
    try:
        result = await session.execute(select(User))
        users = result.scalars().all()
        logger.info(f"Found {len(users)} users.")
        return {"users": users}
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return {"users": []}

async def get_user_by_id_async(session: AsyncSession, user_id: int):
    """
    Get a specific user by ID with detailed information.
    """
    try:
        user = await session.get(User, user_id)
        return user
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None

async def create_user_async(session: AsyncSession, data: dict, admin_user_id: Optional[int] = None):
    """
    Create a new user.
    """
    try:
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return {"success": False, "error": "Username and password are required"}

        existing_user_result = await session.execute(select(User).where(User.username == username))
        if existing_user_result.scalar_one_or_none():
            return {"success": False, "error": "Username already exists"}

        new_user = User(
            username=username,
            phone=data.get("phone"),
            email=data.get("email"),
            is_admin=data.get("is_admin", False),
            force_password_change=data.get("force_password_change", False),
            password_hash=get_password_hash(password)
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        await activity_handlers.record_activity_log(
            session,
            user_id=admin_user_id,
            activity_type_name="user_created",
            activity_category="system",
            title="User Created",
            description=f"User account created: {username}",
            entity_type="user",
            entity_id=new_user.id,
            entity_name=new_user.username,
            is_system_activity=True,
            details={"username": username, "created_by": admin_user_id}
        )

        return {"success": True, "user_id": new_user.id, "message": f"User {username} created successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating user: {e}")
        return {"success": False, "error": str(e)}

async def update_user_async(session: AsyncSession, user_id: int, data: dict, admin_user_id: Optional[int] = None):
    """
    Update an existing user.
    """
    try:
        user = await session.get(User, user_id)
        if not user:
            return {"success": False, "error": "User not found"}

        original_username = user.username
        user.username = data.get("username", user.username)
        user.phone = data.get("phone", user.phone)
        user.email = data.get("email", user.email)
        user.is_admin = data.get("is_admin", user.is_admin)
        user.force_password_change = data.get("force_password_change", user.force_password_change)
        user.updated_at = datetime.now(timezone.utc)

        if new_password := data.get("password"):
            user.password_hash = get_password_hash(new_password)

        await session.commit()

        await activity_handlers.record_activity_log(
            session,
            user_id=admin_user_id,
            activity_type_name="user_updated",
            activity_category="system",
            title="User Updated",
            description=f"User account updated: {user.username}",
            entity_type="user",
            entity_id=user.id,
            entity_name=user.username,
            is_system_activity=True,
            details={"username": user.username, "updated_by": admin_user_id}
        )

        return {"success": True, "message": f"User {user.username} updated successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating user: {e}")
        return {"success": False, "error": str(e)}

async def delete_user_async(session: AsyncSession, user_id: int, admin_user_id: Optional[int] = None):
    """
    Delete a user.
    """
    try:
        user = await session.get(User, user_id)
        if not user:
            return {"success": False, "error": "User not found"}

        if user.is_admin:
            admin_count_result = await session.execute(select(func.count(User.id)).where(User.is_admin == True))
            if admin_count_result.scalar_one() <= 1:
                return {"success": False, "error": "Cannot delete the last admin user"}

        username = user.username
        await session.delete(user)
        
        await activity_handlers.record_activity_log(
            session,
            user_id=admin_user_id,
            activity_type_name="user_deleted",
            activity_category="system",
            title="User Deleted",
            description=f"User account deleted: {username}",
            entity_type="user",
            entity_id=user_id,
            entity_name=username,
            is_system_activity=True,
            details={"username": username, "deleted_by": admin_user_id}
        )
        await session.commit()

        return {"success": True, "message": f"User {username} deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting user: {e}")
        return {"success": False, "error": str(e)}

async def toggle_user_admin_status_async(session: AsyncSession, user_id: int, admin_user_id: Optional[int] = None):
    """
    Toggle admin status for a user.
    """
    try:
        user = await session.get(User, user_id)
        if not user:
            return {"success": False, "error": "User not found"}

        if user.is_admin:
            admin_count_result = await session.execute(select(func.count(User.id)).where(User.is_admin == True))
            if admin_count_result.scalar_one() <= 1:
                return {"success": False, "error": "Cannot remove admin privileges from the last admin user"}

        user.is_admin = not user.is_admin
        user.updated_at = datetime.now(timezone.utc)
        
        status_str = "granted" if user.is_admin else "revoked"
        
        await activity_handlers.record_activity_log(
            session,
            user_id=admin_user_id,
            activity_type_name="admin_status_changed",
            activity_category="system",
            title="Admin Status Changed",
            description=f"Admin status {status_str} for user: {user.username}",
            entity_type="user",
            entity_id=user.id,
            entity_name=user.username,
            is_system_activity=True,
            details={"username": user.username, "new_admin_status": user.is_admin, "changed_by": admin_user_id}
        )
        await session.commit()

        return {"success": True, "is_admin": user.is_admin, "message": f"Successfully {status_str} admin privileges for {user.username}"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error toggling admin status: {e}")
        return {"success": False, "error": str(e)}

async def force_password_reset_async(session: AsyncSession, user_id: int, admin_user_id: Optional[int] = None):
    """
    Force a user to reset their password on next login.
    """
    try:
        user = await session.get(User, user_id)
        if not user:
            return {"success": False, "error": "User not found"}

        user.force_password_change = True
        user.updated_at = datetime.now(timezone.utc)
        
        await activity_handlers.record_activity_log(
            session,
            user_id=admin_user_id,
            activity_type_name="password_reset_forced",
            activity_category="system",
            title="Password Reset Forced",
            description=f"Password reset forced for user: {user.username}",
            entity_type="user",
            entity_id=user.id,
            entity_name=user.username,
            is_system_activity=True,
            details={"username": user.username, "forced_by": admin_user_id}
        )
        await session.commit()

        return {"success": True, "message": f"Password reset forced for {user.username}"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error forcing password reset: {e}")
        return {"success": False, "error": str(e)}

async def get_user_statistics_async(session: AsyncSession):
    """
    Get user statistics for the admin dashboard.
    """
    try:
        total_users_res = await session.execute(select(func.count(User.id)))
        admin_users_res = await session.execute(select(func.count(User.id)).where(User.is_admin == True))
        reset_needed_res = await session.execute(select(func.count(User.id)).where(User.force_password_change == True))
        
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        recent_regs_res = await session.execute(select(func.count(User.id)).where(User.created_at >= thirty_days_ago))

        total_users = total_users_res.scalar_one()
        admin_users = admin_users_res.scalar_one()

        stats = {
            "total_users": total_users,
            "admin_users": admin_users,
            "regular_users": total_users - admin_users,
            "users_needing_password_reset": reset_needed_res.scalar_one(),
            "recent_registrations": recent_regs_res.scalar_one(),
        }
        return {"stats": stats}
    except Exception as e:
        logger.error(f"Error getting user statistics: {e}")
        return {"stats": {
            "total_users": 0, "admin_users": 0, "regular_users": 0,
            "users_needing_password_reset": 0, "recent_registrations": 0,
        }}
