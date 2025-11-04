"""
Settings management handlers for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import Settings, User, SystemActivity


async def get_all_settings(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all settings with their details - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of setting data dictionaries.
    """
    try:
        result = await session.execute(select(Settings).order_by(Settings.key))
        settings = result.scalars().all()

        settings_list = []
        for setting in settings:
            setting_data = {
                "id": setting.id,
                "key": setting.key,
                "value": setting.value,
                "description": setting.description or "",
                "category": getattr(setting, 'category', 'general'),
                "is_public": getattr(setting, 'is_public', False),
                "updated_at": setting.updated_at.strftime("%Y-%m-%d %H:%M:%S") if setting.updated_at else "",
            }
            settings_list.append(setting_data)

        return settings_list
    except Exception as e:
        logger.error(f"Error getting all settings: {e}")
        return []


async def get_setting_by_key(key: str, session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Get a specific setting by key - ASYNC VERSION.

    Args:
        key (str): The key of the setting.
        session: AsyncSession for database operations

    Returns:
        Optional[Dict[str, Any]]: Setting data or None if not found.
    """
    try:
        result = await session.execute(select(Settings).where(Settings.key == key))
        setting = result.scalars().first()
        
        if not setting:
            return None

        setting_data = {
            "id": setting.id,
            "key": setting.key,
            "value": setting.value,
            "description": setting.description or "",
            "category": getattr(setting, 'category', 'general'),
            "is_public": getattr(setting, 'is_public', False),
            "updated_at": setting.updated_at.strftime("%Y-%m-%d %H:%M:%S") if setting.updated_at else "",
        }

        return setting_data
    except Exception as e:
        logger.error(f"Error getting setting by key: {e}")
        return None


async def create_setting(data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Create a new setting - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): Setting data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        # Check if setting key already exists
        existing_result = await session.execute(select(Settings).where(Settings.key == data.get("key")))
        existing = existing_result.scalars().first()
        if existing:
            return {"success": False, "error": "Setting key already exists"}

        # Create new setting
        new_setting = Settings(
            key=data.get("key"),
            value=data.get("value"),
            description=data.get("description"),
        )

        # Add optional fields if they exist
        if hasattr(Settings, 'category') and data.get("category"):
            new_setting.category = data.get("category")
        if hasattr(Settings, 'is_public') and data.get("is_public") is not None:
            new_setting.is_public = data.get("is_public")

        session.add(new_setting)
        await session.commit()
        await session.refresh(new_setting)

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="setting_created",
            details=f"Setting created: {new_setting.key}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "setting_id": new_setting.id,
            "message": f"Setting '{new_setting.key}' created successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating setting: {e}")
        return {"success": False, "error": str(e)}


async def update_setting(key: str, data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Update an existing setting - ASYNC VERSION.

    Args:
        key (str): The key of the setting to update.
        data (Dict[str, Any]): Updated setting data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(Settings).where(Settings.key == key))
        setting = result.scalars().first()
        
        if not setting:
            return {"success": False, "error": "Setting not found"}

        # Update fields
        setting.value = data.get("value", setting.value)
        setting.description = data.get("description", setting.description)
        setting.updated_at = datetime.now()

        # Update optional fields if they exist
        if hasattr(Settings, 'category') and data.get("category") is not None:
            setting.category = data.get("category")
        if hasattr(Settings, 'is_public') and data.get("is_public") is not None:
            setting.is_public = data.get("is_public")

        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="setting_updated",
            details=f"Setting updated: {setting.key}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "message": f"Setting '{setting.key}' updated successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating setting: {e}")
        return {"success": False, "error": str(e)}


async def delete_setting(key: str, session: AsyncSession) -> Dict[str, Any]:
    """
    Delete a setting - ASYNC VERSION.

    Args:
        key (str): The key of the setting to delete.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(Settings).where(Settings.key == key))
        setting = result.scalars().first()
        
        if not setting:
            return {"success": False, "error": "Setting not found"}

        setting_key = setting.key
        await session.delete(setting)
        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=1,  # System user
            type="setting_deleted",
            details=f"Setting deleted: {setting_key}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {"success": True, "message": f"Setting '{setting_key}' deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting setting: {e}")
        return {"success": False, "error": str(e)}


async def get_public_settings(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all public settings - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of public setting data dictionaries.
    """
    try:
        # If is_public field exists, filter by it, otherwise return all
        if hasattr(Settings, 'is_public'):
            result = await session.execute(
                select(Settings).where(Settings.is_public == True).order_by(Settings.key)
            )
        else:
            result = await session.execute(select(Settings).order_by(Settings.key))
        
        settings = result.scalars().all()

        settings_list = []
        for setting in settings:
            setting_data = {
                "key": setting.key,
                "value": setting.value,
            }
            settings_list.append(setting_data)

        return settings_list
    except Exception as e:
        logger.error(f"Error getting public settings: {e}")
        return []


async def get_settings_by_category(category: str, session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get settings by category - ASYNC VERSION.

    Args:
        category (str): The category to filter by.
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of setting data dictionaries.
    """
    try:
        # If category field exists, filter by it
        if hasattr(Settings, 'category'):
            result = await session.execute(
                select(Settings).where(Settings.category == category).order_by(Settings.key)
            )
        else:
            # Fallback: get all settings
            result = await session.execute(select(Settings).order_by(Settings.key))
        
        settings = result.scalars().all()

        settings_list = []
        for setting in settings:
            setting_data = {
                "id": setting.id,
                "key": setting.key,
                "value": setting.value,
                "description": setting.description or "",
                "updated_at": setting.updated_at.strftime("%Y-%m-%d %H:%M:%S") if setting.updated_at else "",
            }
            settings_list.append(setting_data)

        return settings_list
    except Exception as e:
        logger.error(f"Error getting settings by category: {e}")
        return []


async def bulk_update_settings(settings_data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Update multiple settings at once - ASYNC VERSION.

    Args:
        settings_data (Dict[str, Any]): Dictionary of setting keys and values.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        updated_count = 0
        error_count = 0
        errors = []

        for key, value in settings_data.items():
            try:
                result = await session.execute(select(Settings).where(Settings.key == key))
                setting = result.scalars().first()
                
                if setting:
                    setting.value = value
                    setting.updated_at = datetime.now()
                    updated_count += 1
                else:
                    errors.append(f"Setting '{key}' not found")
                    error_count += 1
            except Exception as e:
                errors.append(f"Error updating '{key}': {str(e)}")
                error_count += 1

        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=settings_data.get("user_id", 1),
            type="bulk_settings_updated",
            details=f"Bulk update: {updated_count} settings updated",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "updated_count": updated_count,
            "error_count": error_count,
            "errors": errors if errors else None,
            "message": f"Updated {updated_count} settings successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error in bulk update settings: {e}")
        return {"success": False, "error": str(e)}