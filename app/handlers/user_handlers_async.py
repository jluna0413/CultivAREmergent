"""
User management handlers for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash

from app.logger import logger
from app.models_async import User, SystemActivity, get_async_session
from app.utils.validators import cleanse_user_data


async def get_all_users(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all users with their details and activity summary - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of user data dictionaries.
    """
    try:
        # Use async SQLAlchemy patterns
        result = await session.execute(select(User))
        users = result.scalars().all()

        user_list = []
        for user in users:
            # Get user activity count
            activity_count_result = await session.execute(
                select(SystemActivity).where(SystemActivity.user_id == user.id)
            )
            activities = activity_count_result.scalars().all()
            activity_count = len(activities)

            # Get last activity
            last_activity_result = await session.execute(
                select(SystemActivity)
                .where(SystemActivity.user_id == user.id)
                .order_by(desc(SystemActivity.timestamp))
                .limit(1)
            )
            last_activity = last_activity_result.scalars().first()

            user_data = {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "is_admin": user.is_admin,
                "force_password_change": user.force_password_change,
                "created_at": (
                    user.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if user.created_at
                    else None
                ),
                "updated_at": (
                    user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    if user.updated_at
                    else None
                ),
                "activity_count": activity_count,
                "last_activity": (
                    last_activity.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    if last_activity
                    else None
                ),
                "status": (
                    "Active"
                    if not user.force_password_change
                    else "Password Reset Required"
                ),
            }

            user_list.append(user_data)

        logger.info(f"Found {len(users)} users.")
        logger.info(f"User list: {user_list}")
        return user_list
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []


async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Get a specific user by ID with detailed information - ASYNC VERSION.

    Args:
        user_id (int): The ID of the user.
        session: AsyncSession for database operations

    Returns:
        Optional[Dict[str, Any]]: User data or None if not found.
    """
    try:
        user_result = await session.execute(select(User).where(User.id == user_id))
        user = user_result.scalars().first()
        
        if not user:
            return None

        # Get user activities
        activities_result = await session.execute(
            select(SystemActivity)
            .where(SystemActivity.user_id == user.id)
            .order_by(desc(SystemActivity.timestamp))
            .limit(10)
        )
        activities = activities_result.scalars().all()

        user_data = {
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "is_admin": user.is_admin,
            "force_password_change": user.force_password_change,
            "created_at": (
                user.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if user.created_at
                else None
            ),
            "updated_at": (
                user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                if user.updated_at
                else None
            ),
            "recent_activities": [
                {
                    "type": activity.type,
                    "description": activity.details,
                    "timestamp": activity.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for activity in activities
            ],
        }

        return user_data
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None


async def create_user(data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Create a new user - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): User data containing username, password, phone/email, and role info.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation with success status and user ID.
    """
    try:
        # Cleanse and validate user data
        cleaned_data, validation_errors = cleanse_user_data(data)

        if validation_errors:
            return {"success": False, "error": "; ".join(validation_errors)}

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        is_admin = cleaned_data.get("is_admin", False)
        force_password_change = cleaned_data.get("force_password_change", False)

        # Check if username already exists
        existing_user_result = await session.execute(
            select(User).where(User.username == username)
        )
        existing_user = existing_user_result.scalars().first()
        if existing_user:
            return {"success": False, "error": "Username already exists"}

        # Check if phone/email already exists
        if phone:
            logger.info(f"Checking for existing phone number: {phone}")
            existing_phone_result = await session.execute(
                select(User).where(User.phone == phone)
            )
            existing_phone = existing_phone_result.scalars().first()
            if existing_phone:
                logger.error(f"Phone number {phone} already registered to user {existing_phone.username}")
                return {"success": False, "error": "Phone number already registered"}

        if email:
            existing_email_result = await session.execute(
                select(User).where(User.email == email)
            )
            existing_email = existing_email_result.scalars().first()
            if existing_email:
                return {"success": False, "error": "Email address already registered"}

        # Create new user
        new_user = User(
            username=username,
            phone=phone,
            email=email,
            is_admin=is_admin,
            force_password_change=force_password_change,
        )
        if password:
            new_user.password_hash = generate_password_hash(password)
        else:
            return {"success": False, "error": "Password is required"}

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        # Log system activity
        activity = SystemActivity(
            user_id=new_user.id,
            type="user_created",
            details=f"User account created: {username}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "user_id": new_user.id,
            "message": f"User {username} created successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating user: {e}")
        return {"success": False, "error": str(e)}


async def update_user(user_id: int, data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Update an existing user - ASYNC VERSION.

    Args:
        user_id (int): The ID of the user to update.
        data (Dict[str, Any]): Updated user data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        user_result = await session.execute(select(User).where(User.id == user_id))
        user = user_result.scalars().first()
        if not user:
            return {"success": False, "error": "User not found"}

        # Update basic fields
        user.username = data.get("username", user.username)
        user.phone = data.get("phone", user.phone)
        user.email = data.get("email", user.email)
        user.is_admin = data.get("is_admin", user.is_admin)
        user.force_password_change = data.get(
            "force_password_change", user.force_password_change
        )
        user.updated_at = datetime.now()

        # Update password if provided
        new_password = data.get("password")
        if new_password:
            user.password_hash = generate_password_hash(new_password)
            user.force_password_change = data.get("force_password_change", False)

        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=user.id,
            type="user_updated",
            details=f"User account updated: {user.username}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "message": f"User {user.username} updated successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating user: {e}")
        return {"success": False, "error": str(e)}


async def delete_user(user_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Delete a user (soft delete by deactivating) - ASYNC VERSION.

    Args:
        user_id (int): The ID of the user to delete.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        user_result = await session.execute(select(User).where(User.id == user_id))
        user = user_result.scalars().first()
        if not user:
            return {"success": False, "error": "User not found"}

        # Don't allow deletion of the last admin user
        if user.is_admin:
            admin_count_result = await session.execute(
                select(User).where(User.is_admin == True)
            )
            admin_users = admin_count_result.scalars().all()
            admin_count = len(admin_users)
            if admin_count <= 1:
                return {"success": False, "error": "Cannot delete the last admin user"}

        username = user.username

        # For now, we'll do a hard delete, but in production you might want soft delete
        await session.delete(user)
        await session.commit()

        # Log system activity (need to use a different user_id since this user is deleted)
        admin_user_result = await session.execute(
            select(User).where(User.is_admin == True).limit(1)
        )
        admin_user = admin_user_result.scalars().first()
        if admin_user:
            activity = SystemActivity(
                user_id=admin_user.id,
                type="user_deleted",
                details=f"User account deleted: {username}",
                timestamp=datetime.now(),
            )
            session.add(activity)
            await session.commit()

        return {"success": True, "message": f"User {username} deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting user: {e}")
        return {"success": False, "error": str(e)}


async def toggle_user_admin_status(user_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Toggle admin status for a user - ASYNC VERSION.

    Args:
        user_id (int): The ID of the user.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        user_result = await session.execute(select(User).where(User.id == user_id))
        user = user_result.scalars().first()
        if not user:
            return {"success": False, "error": "User not found"}

        # If removing admin privileges, ensure there's at least one admin left
        if user.is_admin:
            admin_count_result = await session.execute(
                select(User).where(User.is_admin == True)
            )
            admin_users = admin_count_result.scalars().all()
            admin_count = len(admin_users)
            if admin_count <= 1:
                return {
                    "success": False,
                    "error": "Cannot remove admin privileges from the last admin user",
                }

        # Toggle admin status
        user.is_admin = not user.is_admin
        user.updated_at = datetime.now()

        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=user.id,
            type="admin_status_changed",
            details=f'Admin status {"granted to" if user.is_admin else "removed from"} user: {user.username}',
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        status = (
            "granted admin privileges" if user.is_admin else "removed admin privileges"
        )
        return {
            "success": True,
            "message": f"Successfully {status} for {user.username}",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error toggling admin status: {e}")
        return {"success": False, "error": str(e)}


async def force_password_reset(user_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Force a user to reset their password on next login - ASYNC VERSION.

    Args:
        user_id (int): The ID of the user.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        user_result = await session.execute(select(User).where(User.id == user_id))
        user = user_result.scalars().first()
        if not user:
            return {"success": False, "error": "User not found"}

        user.force_password_change = True
        user.updated_at = datetime.now()

        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=user.id,
            type="password_reset_forced",
            details=f"Password reset forced for user: {user.username}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "message": f"Password reset forced for {user.username}",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error forcing password reset: {e}")
        return {"success": False, "error": str(e)}


async def get_user_statistics(session: AsyncSession) -> Dict[str, int]:
    """
    Get user statistics for the admin dashboard - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Dict[str, int]: User statistics.
    """
    try:
        # Get total users
        total_users_result = await session.execute(select(User))
        total_users = len(total_users_result.scalars().all())

        # Get admin users
        admin_users_result = await session.execute(select(User).where(User.is_admin == True))
        admin_users = len(admin_users_result.scalars().all())
        regular_users = total_users - admin_users

        # Get users needing password reset
        password_reset_result = await session.execute(
            select(User).where(User.force_password_change == True)
        )
        users_needing_password_reset = len(password_reset_result.scalars().all())

        # Recent user registrations (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_registrations_result = await session.execute(
            select(User).where(User.created_at >= thirty_days_ago)
        )
        recent_registrations = len(recent_registrations_result.scalars().all())

        return {
            "total_users": total_users,
            "admin_users": admin_users,
            "regular_users": regular_users,
            "users_needing_password_reset": users_needing_password_reset,
            "recent_registrations": recent_registrations,
        }
    except Exception as e:
        logger.error(f"Error getting user statistics: {e}")
        return {
            "total_users": 0,
            "admin_users": 0,
            "regular_users": 0,
            "users_needing_password_reset": 0,
            "recent_registrations": 0,
        }