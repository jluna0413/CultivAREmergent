"""
Async activity handlers for the CultivAR application.
"""

import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.logger import logger
from app.models_async.auth import User # Corrected import for User
from app.models_async.activities import ActivityLog, ActivityType, PlantActivity
from app.models_async.grow import Plant


async def record_activity_log(
    session: AsyncSession,
    activity_type_name: str,
    activity_category: str,
    title: str,
    description: str,
    user_id: Optional[int] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    entity_name: Optional[str] = None,
    is_system_activity: bool = False,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Record an activity log entry.
    """
    try:
        # Determine user_id if not provided
        if user_id is None:
            # This is a system activity, try to find a system user or an admin
            system_user_res = await session.execute(select(User).where(User.username == "system"))
            system_user = system_user_res.scalar_one_or_none()
            if system_user:
                user_id = system_user.id
            else:
                admin_user_res = await session.execute(select(User).where(User.is_admin == True).limit(1))
                admin_user = admin_user_res.scalar_one_or_none()
                if admin_user:
                    user_id = admin_user.id
                else:
                    logger.error("Activity could not be logged: no system or admin user found.")
                    return {"success": False, "error": "Could not determine user for activity."}

        # Get or create ActivityType
        activity_type_obj = await session.execute(select(ActivityType).where(ActivityType.name == activity_type_name))
        activity_type_obj = activity_type_obj.scalar_one_or_none()
        if not activity_type_obj:
            activity_type_obj = ActivityType(
                name=activity_type_name,
                description=description, # Use description from params for new ActivityType
                category=activity_category,
                is_system=is_system_activity
            )
            session.add(activity_type_obj)
            await session.commit()
            await session.refresh(activity_type_obj)

        details_json = None
        if details:
            if isinstance(details, dict):
                details_json = json.dumps(details)
            else:
                details_json = str(details)

        activity_log = ActivityLog(
            user_id=user_id,
            activity_type_id=activity_type_obj.id,
            type=activity_type_name,
            activity_category=activity_category,
            title=title,
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_name=entity_name,
            is_system_activity=is_system_activity,
            details=details_json,
            ip_address=ip_address,
            timestamp=datetime.now(timezone.utc),
        )

        session.add(activity_log)
        await session.commit()
        await session.refresh(activity_log)

        return {"success": True, "activity_id": activity_log.id}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error recording activity log: {e}")
        return {"success": False, "error": str(e)}


async def get_recent_activities(session: AsyncSession, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent system activities.
    """
    try:
        stmt = (
            select(ActivityLog)
            .options(selectinload(ActivityLog.user), selectinload(ActivityLog.activity_type_rel))
            .order_by(desc(ActivityLog.timestamp))
            .limit(limit)
        )
        result = await session.execute(stmt)
        activity_logs = result.scalars().all()

        activities = []
        for activity_log in activity_logs:
            activity_data = {
                "id": activity_log.id,
                "type": activity_log.type,
                "category": activity_log.activity_category,
                "title": activity_log.title,
                "description": activity_log.description,
                "user": activity_log.user.username if activity_log.user else "system",
                "user_id": activity_log.user_id,
                "timestamp": activity_log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "entity_type": activity_log.entity_type,
                "entity_id": activity_log.entity_id,
                "entity_name": activity_log.entity_name,
                "is_system_activity": activity_log.is_system_activity,
                "ip_address": activity_log.ip_address,
            }

            if activity_log.details:
                try:
                    details = json.loads(activity_log.details)
                    activity_data["details"] = details
                except json.JSONDecodeError:
                    activity_data["details"] = activity_log.details
                except Exception as e:
                    logger.warning(f"Could not parse activity details for activity {activity_log.id}: {e}")
                    activity_data["details"] = activity_log.details

            activities.append(activity_data)
        return activities
    except Exception as e:
        logger.error(f"Error getting recent activities: {e}")
        return []


async def get_plant_activities(session: AsyncSession, plant_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent activities for a specific plant.
    """
    try:
        stmt = (
            select(PlantActivity)
            .where(PlantActivity.plant_id == plant_id)
            .options(selectinload(PlantActivity.activity_type_rel), selectinload(PlantActivity.user))
            .order_by(desc(PlantActivity.date))
            .limit(limit)
        )
        result = await session.execute(stmt)
        plant_activities = result.scalars().all()

        activities = []
        for activity in plant_activities:
            activities.append(
                {
                    "id": activity.id,
                    "activity_type": activity.activity_type_rel.name if activity.activity_type_rel else "unknown",
                    "activity_name": activity.activity_name,
                    "note": activity.note,
                    "date": activity.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "user": activity.user.username if activity.user else "system",
                    "user_id": activity.user_id,
                    "ip_address": activity.ip_address,
                }
            )
        return activities
    except Exception as e:
        logger.error(f"Error getting plant activities: {e}")
        return []


async def record_login_activity(session: AsyncSession, username: str, ip_address: Optional[str] = None) -> Dict[str, Any]:
    """Record a login activity."""
    user_res = await session.execute(select(User).where(User.username == username))
    user = user_res.scalar_one_or_none()
    user_id = user.id if user else None
    return await record_activity_log(
        session,
        activity_type_name="user_login",
        activity_category="authentication",
        title="User Login",
        description=f"User {username} logged in.",
        user_id=user_id,
        entity_type="user",
        entity_name=username,
        is_system_activity=True,
        details={"username": username},
        ip_address=ip_address,
    )


async def record_plant_add_activity(session: AsyncSession, plant_name: str, plant_id: int, user_id: Optional[int] = None, ip_address: Optional[str] = None) -> Dict[str, Any]:
    """Record a plant add activity."""
    return await record_activity_log(
        session,
        activity_type_name="plant_added",
        activity_category="plant_management",
        title="Plant Added",
        description=f"New plant '{plant_name}' (ID: {plant_id}) was added.",
        user_id=user_id,
        entity_type="plant",
        entity_id=plant_id,
        entity_name=plant_name,
        is_system_activity=False,
        details={"plant_name": plant_name, "plant_id": plant_id},
        ip_address=ip_address,
    )


async def record_strain_edit_activity(session: AsyncSession, strain_name: str, strain_id: int, user_id: Optional[int] = None, ip_address: Optional[str] = None) -> Dict[str, Any]:
    """Record a strain edit activity."""
    return await record_activity_log(
        session,
        activity_type_name="strain_edited",
        activity_category="strain_management",
        title="Strain Edited",
        description=f"Strain '{strain_name}' (ID: {strain_id}) was edited.",
        user_id=user_id,
        entity_type="cultivar",
        entity_id=strain_id,
        entity_name=strain_name,
        is_system_activity=False,
        details={"strain_name": strain_name, "strain_id": strain_id},
        ip_address=ip_address,
    )


async def record_user_add_activity(session: AsyncSession, new_username: str, user_id: Optional[int] = None, ip_address: Optional[str] = None) -> Dict[str, Any]:
    """Record a user add activity."""
    return await record_activity_log(
        session,
        activity_type_name="user_added",
        activity_category="user_management",
        title="User Added",
        description=f"New user '{new_username}' was added.",
        user_id=user_id,
        entity_type="user",
        entity_name=new_username,
        is_system_activity=True,
        details={"new_username": new_username},
        ip_address=ip_address,
    )


async def record_sensor_reading_activity(session: AsyncSession, sensor_name: str, value: Any, unit: str, user_id: Optional[int] = None, ip_address: Optional[str] = None) -> Dict[str, Any]:
    """Record a sensor reading activity."""
    return await record_activity_log(
        session,
        activity_type_name="sensor_reading",
        activity_category="sensor_data",
        title="Sensor Reading",
        description=f"Sensor '{sensor_name}' recorded a reading: {value}{unit}.",
        user_id=user_id,
        entity_type="sensor",
        entity_name=sensor_name,
        is_system_activity=True,
        details={"sensor_name": sensor_name, "value": value, "unit": unit},
        ip_address=ip_address,
    )


async def record_plant_activity(session: AsyncSession, plant_id: int, activity_name: str, note: Optional[str] = None, user_id: Optional[int] = None, ip_address: Optional[str] = None) -> Dict[str, Any]:
    """Record a plant activity."""
    try:
        plant = await session.get(Plant, plant_id)
        if not plant:
            return {"success": False, "error": "Plant not found"}

        return await record_activity_log(
            session,
            activity_type_name=activity_name.lower().replace(" ", "_"), # Convert activity name to a suitable type name
            activity_category="plant_management",
            title=activity_name,
            description=f"Plant '{plant.name}' (ID: {plant_id}) activity: {activity_name}. Note: {note or 'N/A'}",
            user_id=user_id,
            entity_type="plant",
            entity_id=plant_id,
            entity_name=plant.name,
            is_system_activity=False,
            details={"plant_name": plant.name, "plant_id": plant_id, "activity_name": activity_name, "note": note},
            ip_address=ip_address,
        )
    except Exception as e:
        logger.error(f"Error recording plant activity: {e}")
        return {"success": False, "error": str(e)}
