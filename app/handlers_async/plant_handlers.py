"""
Async plant handlers for the CultivAR application.
"""

import os
from datetime import datetime, timezone
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from fastapi import UploadFile
import aiofiles
from werkzeug.utils import secure_filename

from app.config.config import Config
from app.logger import logger
from app.models_async.activities import PlantActivity, ActivityType
from app.models_async.grow import Plant, PlantImage, Measurement, Status
from app.models_async.sensors import Sensor
from app.utils.helpers import (
    calculate_days_since,
    calculate_weeks_since,
    estimate_harvest_date,
)
from app.utils.security import validate_uploaded_file, SecurityValidationError, validate_filename
import uuid
from datetime import datetime

# --- Read Operations ---

async def get_plant(session: AsyncSession, plant_id: int):
    """
    Get a plant by ID with all its related data.
    """
    try:
        stmt = (
            select(Plant)
            .where(Plant.id == plant_id)
            .options(
                selectinload(Plant.measurements),
                selectinload(Plant.activities).selectinload(PlantActivity.activity_type_rel),
                selectinload(Plant.images),
                selectinload(Plant.status),
                selectinload(Plant.cultivar).selectinload('breeder'),
                selectinload(Plant.zone),
                selectinload(Plant.parent),
            )
        )
        result = await session.execute(stmt)
        plant = result.scalar_one_or_none()

        if not plant:
            return None

        # The properties on the model will handle most of this, but we can add more complex calculations here.
        plant_data = {
            "id": plant.id,
            "name": plant.name,
            "description": plant.description,
            "status_name": plant.status_name,
            "strain_name": plant.strain_name,
            "breeder_name": plant.breeder_name,
            "zone_name": plant.zone_name,
            "current_day": calculate_days_since(plant.start_dt),
            "current_week": calculate_weeks_since(plant.start_dt),
            "est_harvest_date": estimate_harvest_date(plant.start_dt, plant.cycle_time, plant.autoflower),
            "latest_image_url": plant.latest_image.image_path if plant.latest_image else None,
            # Add other fields as needed
        }
        return plant_data
    except Exception as e:
        logger.error(f"Error getting plant: {e}")
        return None

async def get_living_plants(session: AsyncSession):
    """
    Get all living plants (not harvested or dead).
    """
    try:
        stmt = select(Plant).where(Plant.status_id.notin_([4, 5])).options(selectinload(Plant.cultivar))
        result = await session.execute(stmt)
        plants = result.scalars().all()
        
        # This can be simplified if the data is processed on the client
        return [
            {
                "id": p.id,
                "name": p.name,
                "strain_name": p.strain_name,
                "current_day": calculate_days_since(p.start_dt),
                "status": p.status_name,
            }
            for p in plants
        ]
    except Exception as e:
        logger.error(f"Error getting living plants: {e}")
        return []

# ... other get functions (get_harvested_plants, get_dead_plants, etc.) would follow a similar pattern ...

# --- Write Operations ---

async def add_plant(session: AsyncSession, data: dict):
    """
    Add a new plant.
    """
    try:
        status_id = data.get("status_id", 1)  # Default to 'Seedling'
        new_plant = Plant(
            name=data.get("name"),
            description=data.get("description"),
            status_id=status_id,
            strain_id=data.get("strain_id"),
            zone_id=data.get("zone_id"),
            is_clone=data.get("is_clone", False),
            autoflower=data.get("autoflower", False),
            parent_id=data.get("parent_id"),
            start_dt=datetime.now(timezone.utc),
        )
        session.add(new_plant)
        await session.commit()
        await session.refresh(new_plant)
        return {"success": True, "id": new_plant.id}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error adding plant: {e}")
        return {"success": False, "error": str(e)}


async def update_plant(session: AsyncSession, plant_id: int, data: dict):
    """
    Update a plant.
    """
    try:
        plant = await session.get(Plant, plant_id)
        if not plant:
            return {"success": False, "error": "Plant not found"}

        for key, value in data.items():
            if hasattr(plant, key):
                setattr(plant, key, value)
        
        plant.updated_at = datetime.now(timezone.utc)

        await session.commit()
        return {"success": True, "plant_id": plant.id}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating plant: {e}")
        return {"success": False, "error": str(e)}


async def delete_plant(session: AsyncSession, plant_id: int):
    """
    Delete a plant and its associated data and files.
    """
    try:
        plant = await session.get(Plant, plant_id, options=[selectinload(Plant.images)])
        if not plant:
            return {"success": False, "error": "Plant not found"}

        # Delete image files from disk (this is blocking, consider a background task)
        for image in plant.images:
            # Construct absolute path
            image_path = os.path.join(Config.UPLOAD_FOLDER, "plants", str(plant_id), os.path.basename(image.image_path))
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except OSError as e:
                    logger.error(f"Error deleting image file {image_path}: {e}")
        
        # SQLAlchemy with cascade delete will handle associated records
        await session.delete(plant)
        await session.commit()

        return {"success": True}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting plant: {e}")
        return {"success": False, "error": str(e)}


def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

async def upload_plant_images(session: AsyncSession, plant_id: int, files: List[UploadFile], description: str):
    """
    Upload images for a plant asynchronously with comprehensive security validation.
    """
    try:
        plant = await session.get(Plant, plant_id)
        if not plant:
            return {"success": False, "error": "Plant not found"}

        upload_folder = os.path.join(Config.UPLOAD_FOLDER, "plants", str(plant_id))
        os.makedirs(upload_folder, exist_ok=True)

        uploaded_images = []
        for file in files:
            if not file.filename or not allowed_file(file.filename):
                logger.warning(f"Skipping invalid file: {file.filename}")
                continue

            # Check file size by reading the content
            content = await file.read()
            if len(content) > 10 * 1024 * 1024:  # 10MB limit
                logger.warning(f"File too large: {file.filename}")
                continue

            # Validate the uploaded file using our security utility
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            try:
                validate_uploaded_file(
                    file_content=content,
                    filename=file.filename,
                    allowed_extensions=allowed_extensions
                )
            except SecurityValidationError as e:
                logger.warning(f"File validation failed for {file.filename}: {e}")
                continue

            # Generate secure filename to prevent path traversal
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
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
                logger.warning(f"Path traversal attempt detected: {file.filename}")
                continue
            
            # Asynchronously write the file
            async with aiofiles.open(file_path, 'wb') as out_file:
                await out_file.write(content)

            db_path = os.path.join("uploads", "plants", str(plant_id), unique_filename).replace("\\", "/")
            
            new_image = PlantImage(
                plant_id=plant_id,
                image_path=db_path,
                image_description=description,
                image_date=datetime.now(timezone.utc),
            )
            session.add(new_image)
            uploaded_images.append(new_image)
        
        await session.commit()
        for img in uploaded_images:
            await session.refresh(img)

        return {
            "success": True,
            "images": [{"id": img.id, "image_path": img.image_path} for img in uploaded_images],
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error uploading plant images: {e}")
        return {"success": False, "error": str(e)}

async def delete_plant_image(session: AsyncSession, image_id: int):
    """
    Delete a plant image from the database and disk.
    """
    try:
        image = await session.get(PlantImage, image_id)
        if not image:
            return {"success": False, "error": "Image not found"}

        # Blocking file operation
        image_path = os.path.join(Config.BASE_DIR, image.image_path)
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError as e:
                logger.error(f"Error deleting image file {image_path}: {e}")

        await session.delete(image)
        await session.commit()
        return {"success": True}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting plant image: {e}")
        return {"success": False, "error": str(e)}

async def record_activity(session: AsyncSession, data: dict):
    """
    Record a plant activity.
    """
    try:
        plant_id = data.get("plant_id")
        activity_id = data.get("activity_id")
        note = data.get("note", "")

        if not plant_id or not activity_id:
            return {"success": False, "error": "Plant ID and Activity ID are required"}

        plant = await session.get(Plant, plant_id)
        if not plant:
            return {"success": False, "error": "Plant not found"}
            
        activity_type = await session.get(ActivityType, activity_id)
        if not activity_type:
            return {"success": False, "error": "Activity type not found"}

        new_activity = PlantActivity(
            plant_id=plant_id,
            activity_type_id=activity_id,
            activity_name=activity_type.name,
            note=note,
            date=datetime.now(timezone.utc),
        )
        session.add(new_activity)
        
        # Update plant based on activity
        if activity_type.name.lower() in ["watering", "water"]:
            plant.last_water_date = datetime.now(timezone.utc)
        elif activity_type.name.lower() in ["feeding", "feed"]:
            plant.last_feed_date = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(new_activity)
        
        return {"success": True, "activity_id": new_activity.id}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error recording plant activity: {e}")
        return {"success": False, "error": str(e)}

# Other handlers like link_sensors_to_plant would be converted similarly.
