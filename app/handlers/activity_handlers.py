"""
Activity handlers for the CultivAR application.
"""

import json
from datetime import datetime

from flask_login import current_user

from app.logger import logger
from app.models import db
from app.models.base_models import Plant, PlantActivity, User
from app.models.system_models import SystemActivity


def record_system_activity(activity_type, details=None, user_id=None):
    """
    Record a system activity.

    Args:
        activity_type (str): The type of activity (login, plant_add, etc.)
        details (dict): Details about the activity
        user_id (int): The ID of the user who performed the activity

    Returns:
        dict: The result of the operation
    """
    try:
        # Get the current user if not provided
        if user_id is None and current_user and hasattr(current_user, "id"):
            user_id = current_user.id
        elif user_id is None:
            # This is a system activity, find the system user or an admin
            system_user = User.query.filter_by(username="system").first()
            if not system_user:
                admin_user = User.query.filter_by(is_admin=True).first()
                if admin_user:
                    user_id = admin_user.id
                else:
                    # Fallback if no admin is found, though this should not happen in a configured system
                    logger.error(
                        "System activity could not be logged: no system or admin user found."
                    )
                    return {
                        "success": False,
                        "error": "Could not determine user for system activity.",
                    }
            else:
                user_id = system_user.id

        # Convert details to JSON string if it's a dict
        details_json = None
        if details:
            if isinstance(details, dict):
                details_json = json.dumps(details)
            else:
                details_json = str(details)

        # Create a new system activity
        activity = SystemActivity(
            type=activity_type,
            user_id=user_id,
            details=details_json,
            timestamp=datetime.utcnow(),
        )

        # Add the activity to the database
        db.session.add(activity)
        db.session.commit()

        return {"success": True, "activity_id": activity.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error recording system activity: {e}")
        return {"success": False, "error": str(e)}


def get_recent_activities(limit=10):
    """
    Get recent system activities.

    Args:
        limit (int): The maximum number of activities to return

    Returns:
        list: A list of recent activities
    """
    try:
        # Get recent system activities
        system_activities = (
            SystemActivity.query.order_by(SystemActivity.timestamp.desc())
            .limit(limit)
            .all()
        )

        activities = []
        for activity in system_activities:
            activity_data = {
                "type": activity.type,
                "user": activity.user.username if activity.user else "system",
                "timestamp": activity.timestamp,
            }

            # Parse details if available
            if activity.details:
                try:
                    details = json.loads(activity.details)
                    activity_data.update(details)
                except:
                    # If details is not valid JSON, just use it as is
                    activity_data["details"] = activity.details

            activities.append(activity_data)

        return activities
    except Exception as e:
        logger.error(f"Error getting recent activities: {e}")
        return []


def get_plant_activities(plant_id, limit=10):
    """
    Get recent activities for a specific plant.

    Args:
        plant_id (int): The ID of the plant
        limit (int): The maximum number of activities to return

    Returns:
        list: A list of recent plant activities
    """
    try:
        # Get recent plant activities
        plant_activities = (
            PlantActivity.query.filter_by(plant_id=plant_id)
            .order_by(PlantActivity.date.desc())
            .limit(limit)
            .all()
        )

        activities = []
        for activity in plant_activities:
            activities.append(
                {
                    "id": activity.id,
                    "name": activity.name,
                    "note": activity.note,
                    "date": activity.date,
                    "activity_id": activity.activity_id,
                }
            )

        return activities
    except Exception as e:
        logger.error(f"Error getting plant activities: {e}")
        return []


def record_login_activity(username):
    """Record a login activity."""
    user = User.query.filter_by(username=username).first()
    user_id = user.id if user else None
    return record_system_activity("login", user_id=user_id)


def record_plant_add_activity(plant_name, plant_id):
    """Record a plant add activity."""
    return record_system_activity(
        "plant_add", {"plant": plant_name, "plant_id": plant_id}
    )


def record_cultivar_edit_activity(cultivar_name, cultivar_id):
    """Record a cultivar edit activity."""
    return record_system_activity(
        "cultivar_edit", {"cultivar": cultivar_name, "cultivar_id": cultivar_id}
    )


# Backward compatibility alias
def record_strain_edit_activity(strain_name, strain_id):
    """Record a strain edit activity. (Deprecated - use record_cultivar_edit_activity)"""
    return record_cultivar_edit_activity(strain_name, strain_id)


def record_user_add_activity(new_username):
    """Record a user add activity."""
    return record_system_activity("user_add", {"new_user": new_username})


def record_sensor_reading_activity(sensor_name, value, unit):
    """Record a sensor reading activity."""
    return record_system_activity(
        "sensor_reading", {"sensor": sensor_name, "value": f"{value}{unit}"}
    )


def record_plant_activity(plant_id, activity_name, note=None):
    """Record a plant activity."""
    try:
        plant = Plant.query.get(plant_id)
        if not plant:
            return {"success": False, "error": "Plant not found"}

        return record_system_activity(
            "plant_activity",
            {
                "plant": plant.name,
                "plant_id": plant_id,
                "activity": activity_name,
                "note": note,
            },
        )
    except Exception as e:
        logger.error(f"Error recording plant activity: {e}")
        return {"success": False, "error": str(e)}
