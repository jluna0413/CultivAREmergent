"""
Activity management handlers for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import PlantActivity, Plant, User, SystemActivity


async def get_all_activities(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all plant activities with their details - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of activity data dictionaries.
    """
    try:
        result = await session.execute(select(PlantActivity).order_by(desc(PlantActivity.created_at)))
        activities = result.scalars().all()

        activity_list = []
        for activity in activities:
            activity_data = {
                "id": activity.id,
                "plant_id": activity.plant_id,
                "plant_name": activity.plant_name or (activity.plant.name if activity.plant else ""),
                "activity_type": activity.activity_type,
                "activity_name": activity.activity_name,
                "note": activity.note or "",
                "created_at": activity.created_at.strftime("%Y-%m-%d %H:%M:%S") if activity.created_at else "",
                "user_id": activity.user_id,
            }
            activity_list.append(activity_data)

        return activity_list
    except Exception as e:
        logger.error(f"Error getting all activities: {e}")
        return []


async def get_activities_by_plant(plant_id: int, session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get activities for a specific plant - ASYNC VERSION.

    Args:
        plant_id (int): The ID of the plant.
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of activity data dictionaries.
    """
    try:
        result = await session.execute(
            select(PlantActivity).where(PlantActivity.plant_id == plant_id).order_by(desc(PlantActivity.created_at))
        )
        activities = result.scalars().all()

        activity_list = []
        for activity in activities:
            activity_data = {
                "id": activity.id,
                "plant_id": activity.plant_id,
                "type": getattr(activity, 'type', ''),
                "name": activity.name,
                "note": activity.note or "",
                "created_at": activity.created_at.strftime("%Y-%m-%d %H:%M:%S") if activity.created_at else "",
            }
            activity_list.append(activity_data)

        return activity_list
    except Exception as e:
        logger.error(f"Error getting activities by plant: {e}")
        return []


async def create_activity(data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Create a new plant activity - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): Activity data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        # Create new activity
        new_activity = PlantActivity(
            plant_id=data.get("plant_id"),
            name=data.get("name"),
            note=data.get("note"),
            user_id=data.get("user_id"),
        )

        # Add type field if it exists
        if hasattr(PlantActivity, 'type') and data.get("type"):
            new_activity.type = data.get("type")

        session.add(new_activity)
        await session.commit()
        await session.refresh(new_activity)

        # Log system activity
        system_activity = SystemActivity(
            user_id=data.get("user_id"),
            type="activity_created",
            details=f"Activity created for plant {data.get('plant_id')}: {new_activity.name}",
            timestamp=datetime.now(),
        )
        session.add(system_activity)
        await session.commit()

        return {
            "success": True,
            "activity_id": new_activity.id,
            "message": f"Activity '{new_activity.name}' created successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating activity: {e}")
        return {"success": False, "error": str(e)}


async def update_activity(activity_id: int, data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Update an existing activity - ASYNC VERSION.

    Args:
        activity_id (int): The ID of the activity to update.
        data (Dict[str, Any]): Updated activity data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(PlantActivity).where(PlantActivity.id == activity_id))
        activity = result.scalars().first()
        
        if not activity:
            return {"success": False, "error": "Activity not found"}

        # Update fields
        activity.name = data.get("name", activity.name)
        activity.note = data.get("note", activity.note)

        # Update type field if it exists
        if hasattr(PlantActivity, 'type') and data.get("type") is not None:
            activity.type = data.get("type")

        await session.commit()

        # Log system activity
        system_activity = SystemActivity(
            user_id=data.get("user_id"),
            type="activity_updated",
            details=f"Activity updated: {activity.name}",
            timestamp=datetime.now(),
        )
        session.add(system_activity)
        await session.commit()

        return {
            "success": True,
            "message": f"Activity '{activity.name}' updated successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating activity: {e}")
        return {"success": False, "error": str(e)}


async def delete_activity(activity_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Delete an activity - ASYNC VERSION.

    Args:
        activity_id (int): The ID of the activity to delete.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(PlantActivity).where(PlantActivity.id == activity_id))
        activity = result.scalars().first()
        
        if not activity:
            return {"success": False, "error": "Activity not found"}

        activity_name = activity.name
        await session.delete(activity)
        await session.commit()

        # Log system activity
        system_activity = SystemActivity(
            user_id=1,  # System user
            type="activity_deleted",
            details=f"Activity deleted: {activity_name}",
            timestamp=datetime.now(),
        )
        session.add(system_activity)
        await session.commit()

        return {"success": True, "message": f"Activity '{activity_name}' deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting activity: {e}")
        return {"success": False, "error": str(e)}


async def get_recent_activities(limit: int = 10, session: AsyncSession = None) -> List[Dict[str, Any]]:
    """
    Get recent activities - ASYNC VERSION.

    Args:
        limit (int): Maximum number of activities to return.
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of recent activity data dictionaries.
    """
    try:
        result = await session.execute(
            select(PlantActivity).order_by(desc(PlantActivity.created_at)).limit(limit)
        )
        activities = result.scalars().all()

        activity_list = []
        for activity in activities:
            activity_data = {
                "id": activity.id,
                "plant_id": activity.plant_id,
                "plant_name": activity.plant.name if activity.plant else "",
                "type": getattr(activity, 'type', ''),
                "name": activity.name,
                "note": activity.note or "",
                "created_at": activity.created_at.strftime("%Y-%m-%d %H:%M:%S") if activity.created_at else "",
            }
            activity_list.append(activity_data)

        return activity_list
    except Exception as e:
        logger.error(f"Error getting recent activities: {e}")
        return []


async def get_activity_statistics(session: AsyncSession) -> Dict[str, int]:
    """
    Get activity-related statistics - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Dict[str, int]: Activity statistics.
    """
    try:
        # Get total activities
        all_activities_result = await session.execute(select(PlantActivity))
        all_activities = all_activities_result.scalars().all()

        # Get activities from last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_activities_result = await session.execute(
            select(PlantActivity).where(PlantActivity.created_at >= seven_days_ago)
        )
        recent_activities = recent_activities_result.scalars().all()

        # Get unique plants with activities
        plants_with_activities = set()
        for activity in all_activities:
            if activity.plant_id:
                plants_with_activities.add(activity.plant_id)

        stats = {
            "total_activities": len(all_activities),
            "recent_activities": len(recent_activities),
            "plants_with_activities": len(plants_with_activities),
        }

        return stats
    except Exception as e:
        logger.error(f"Error getting activity statistics: {e}")
        return {
            "total_activities": 0,
            "recent_activities": 0,
            "plants_with_activities": 0,
        }


async def search_activities(query: str, session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Search activities by name or note - ASYNC VERSION.

    Args:
        query (str): Search query.
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of matching activity data dictionaries.
    """
    try:
        # Simple search by name and note (in a real app, you'd want full-text search)
        result = await session.execute(select(PlantActivity))
        all_activities = result.scalars().all()

        matching_activities = []
        query_lower = query.lower()

        for activity in all_activities:
            if (query_lower in activity.name.lower() or 
                (activity.note and query_lower in activity.note.lower())):
                
                activity_data = {
                    "id": activity.id,
                    "plant_id": activity.plant_id,
                    "plant_name": activity.plant.name if activity.plant else "",
                    "type": getattr(activity, 'type', ''),
                    "name": activity.name,
                    "note": activity.note or "",
                    "created_at": activity.created_at.strftime("%Y-%m-%d %H:%M:%S") if activity.created_at else "",
                }
                matching_activities.append(activity_data)

        return matching_activities
    except Exception as e:
        logger.error(f"Error searching activities: {e}")
        return []