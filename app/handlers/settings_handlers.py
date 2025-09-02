"""
Settings handlers for the CultivAR application.
"""

import os

from werkzeug.utils import secure_filename

from app.config.config import Config
from app.logger import logger
from app.models import db
from app.models.base_models import Settings, User

# from app.utils.auth import hash_password # Make sure this line is commented out or removed
from app.utils.image import save_image


def get_settings():
    """
    Get all settings.

    Returns:
        dict: The settings.
    """
    try:
        # Get all settings
        settings_records = Settings.query.all()

        # Convert to dictionary
        settings = {}
        for record in settings_records:
            settings[record.key] = record.value

        # Format settings
        formatted_settings = {
            "aci": {
                "enabled": settings.get("aci_enabled", "false").lower() == "true",
                "token_set": settings.get("aci_token", "") != "",
            },
            "ec": {
                "enabled": settings.get("ec_enabled", "false").lower() == "true",
                "server": settings.get("ec_server", ""),
            },
            "polling_interval": int(settings.get("polling_interval", "300")),
            "guest_mode": settings.get("guest_mode", "false").lower() == "true",
            "stream_grab_enabled": settings.get("stream_grab_enabled", "false").lower()
            == "true",
            "stream_grab_interval": int(settings.get("stream_grab_interval", "3600")),
        }

        return formatted_settings
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return {}


def get_setting(key):
    """
    Get a setting by key.

    Args:
        key (str): The setting key.

    Returns:
        str: The setting value.
    """
    try:
        setting = Settings.query.filter_by(key=key).first()
        return setting.value if setting else None
    except Exception as e:
        logger.error(f"Error getting setting: {e}")
        return None


def update_setting(key, value):
    """
    Update a setting.

    Args:
        key (str): The setting key.
        value (str): The setting value.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        setting = Settings.query.filter_by(key=key).first()

        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
            db.session.add(setting)

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating setting: {e}")
        return False


def exists_setting(key):
    """
    Check if a setting exists.

    Args:
        key (str): The setting key.

    Returns:
        bool: True if the setting exists, False otherwise.
    """
    try:
        setting = Settings.query.filter_by(key=key).first()
        return setting is not None
    except Exception as e:
        logger.error(f"Error checking if setting exists: {e}")
        return False


def save_settings(data):
    """
    Save settings.

    Args:
        data (dict): The settings data.

    Returns:
        dict: The result of the operation.
    """
    try:
        # Update AC Infinity settings
        aci = data.get("aci", {})
        update_setting("aci_enabled", str(aci.get("enabled", False)).lower())

        # Update Ecowitt settings
        ec = data.get("ec", {})
        update_setting("ec_enabled", str(ec.get("enabled", False)).lower())
        update_setting("ec_server", ec.get("server", ""))

        # Update other settings
        update_setting("polling_interval", str(data.get("polling_interval", 300)))
        update_setting("guest_mode", str(data.get("guest_mode", False)).lower())
        update_setting(
            "stream_grab_enabled", str(data.get("stream_grab_enabled", False)).lower()
        )
        update_setting(
            "stream_grab_interval", str(data.get("stream_grab_interval", 3600))
        )

        return {"success": True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error saving settings: {e}")
        return {"success": False, "error": str(e)}


def update_user_password(user_id, password):
    """
    Update a user's password.

    Args:
        user_id (int): The ID of the user.
        password (str): The new password.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        user = db.session.get(User, user_id)

        if not user:
            return False

        # Update the user
        user.set_password(password)  # Use the User model's method to hash and set
        user.force_password_change = False

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user password: {e}")
        return False


def upload_logo(file):
    """
    Upload a logo.

    Args:
        file: The logo file.

    Returns:
        dict: The result of the operation.
    """
    try:
        if not file:
            return {"success": False, "error": "No file provided"}

        # Create the upload folder if it doesn't exist
        upload_folder = os.path.join(Config.UPLOAD_FOLDER, "logos")
        os.makedirs(upload_folder, exist_ok=True)

        # Generate a secure filename
        filename = secure_filename(file.filename)

        # Save the file
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Update the logo setting
        update_setting("logo", os.path.join("uploads", "logos", filename))

        return {
            "success": True,
            "logo_path": os.path.join("uploads", "logos", filename),
        }
    except Exception as e:
        logger.error(f"Error uploading logo: {e}")
        return {"success": False, "error": str(e)}
