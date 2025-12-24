"""
Async settings handlers for the CultivAR application.
"""

import os
import json
from typing import Dict, Any, Optional
from fastapi import UploadFile
import aiofiles
from werkzeug.utils import secure_filename

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.config import Config
from app.logger import logger
from app.models_async.settings import Settings
from app.models_async.auth import User
from app.handlers_async.user_handlers import get_password_hash # For password hashing
from app.utils.security import validate_uploaded_file, SecurityValidationError, validate_filename
import uuid
from datetime import datetime


async def get_settings(session: AsyncSession) -> Dict[str, Any]:
    """
    Get all settings.
    """
    try:
        result = await session.execute(select(Settings))
        settings_records = result.scalars().all()

        settings = {}
        for record in settings_records:
            settings[record.key] = record.value

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
            "stream_grab_enabled": settings.get("stream_grab_enabled", "false").lower() == "true",
            "stream_grab_interval": int(settings.get("stream_grab_interval", "3600")),
        }
        return formatted_settings
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return {}


async def get_setting(session: AsyncSession, key: str) -> Optional[str]:
    """
    Get a setting by key.
    """
    try:
        result = await session.execute(select(Settings).where(Settings.key == key))
        setting = result.scalar_one_or_none()
        return setting.value if setting else None
    except Exception as e:
        logger.error(f"Error getting setting: {e}")
        return None


async def update_setting(session: AsyncSession, key: str, value: str) -> bool:
    """
    Update a setting.
    """
    try:
        result = await session.execute(select(Settings).where(Settings.key == key))
        setting = result.scalar_one_or_none()

        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
            session.add(setting)

        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating setting: {e}")
        return False


async def exists_setting(session: AsyncSession, key: str) -> bool:
    """
    Check if a setting exists.
    """
    try:
        result = await session.execute(select(Settings).where(Settings.key == key))
        setting = result.scalar_one_or_none()
        return setting is not None
    except Exception as e:
        logger.error(f"Error checking if setting exists: {e}")
        return False


async def save_settings(session: AsyncSession, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save settings.
    """
    try:
        aci = data.get("aci", {})
        await update_setting(session, "aci_enabled", str(aci.get("enabled", False)).lower())

        ec = data.get("ec", {})
        await update_setting(session, "ec_enabled", str(ec.get("enabled", False)).lower())
        await update_setting(session, "ec_server", ec.get("server", ""))

        await update_setting(session, "polling_interval", str(data.get("polling_interval", 300)))
        await update_setting(session, "guest_mode", str(data.get("guest_mode", False)).lower())
        await update_setting(session, "stream_grab_enabled", str(data.get("stream_grab_enabled", False)).lower())
        await update_setting(session, "stream_grab_interval", str(data.get("stream_grab_interval", 3600)))

        return {"success": True}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error saving settings: {e}")
        return {"success": False, "error": str(e)}


async def update_user_password(session: AsyncSession, user_id: int, password: str) -> bool:
    """
    Update a user's password.
    """
    try:
        user = await session.get(User, user_id)
        if not user:
            return False

        user.password_hash = get_password_hash(password)
        user.force_password_change = False

        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating user password: {e}")
        return False

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


async def upload_logo(session: AsyncSession, file: UploadFile) -> Dict[str, Any]:
    """
    Upload a logo with comprehensive security validation.
    """
    try:
        if not file:
            return {"success": False, "error": "No file provided"}

        # Check file size by reading the content
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            return {"success": False, "error": "File too large (max 10MB)"}

        # Validate the uploaded file using our security utility
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
        try:
            validate_uploaded_file(
                file_content=content,
                filename=file.filename,
                allowed_extensions=allowed_extensions
            )
        except SecurityValidationError as e:
            return {"success": False, "error": f"File validation failed: {str(e)}"}

        # Additional content type validation
        if file.content_type not in Config.ALLOWED_MIME_TYPES:
            return {"success": False, "error": "Invalid file type"}

        upload_folder = os.path.join(Config.UPLOAD_FOLDER, "logos")
        os.makedirs(upload_folder, exist_ok=True)

        # Generate secure filename to prevent path traversal
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{uuid.uuid4().hex}"
        
        # Add extension securely
        if '.' in file.filename:
            extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{unique_filename}.{extension}"
        
        file_path = os.path.join(upload_folder, unique_filename)

        # Verify path is within upload folder (extra security)
        file_path = os.path.abspath(file_path)
        upload_folder_abs = os.path.abspath(upload_folder)
        if not file_path.startswith(upload_folder_abs):
            return {"success": False, "error": "Invalid file path"}

        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(content)

        db_path = os.path.join("uploads", "logos", unique_filename).replace("\\", "/")
        await update_setting(session, "logo", db_path)

        return {"success": True, "logo_path": db_path}
    except Exception as e:
        logger.error(f"Error uploading logo: {e}")
        return {"success": False, "error": str(e)}

