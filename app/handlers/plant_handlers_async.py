"""
Plant handlers for the CultivAR application - ASYNC VERSION.
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import select, desc, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI

from app.config.config import Config
from app.logger import logger
from app.models_async import Plant, Cultivar, Status, Zone, User, PlantActivity, PlantImage, Measurement, SystemActivity, get_async_session
from app.utils.helpers import (
    calculate_days_since,
    calculate_weeks_since,
    estimate_harvest_date,
)


async def get_plant(plant_id: int, session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Get a plant by ID - ASYNC VERSION.

    Args:
        plant_id (int): The ID of the plant.
        session: AsyncSession for database operations

    Returns:
        Optional[Dict[str, Any]]: The plant data or None if not found.
    """
    try:
        plant_result = await session.execute(select(Plant).where(Plant.id == plant_id))
        plant = plant_result.scalars().first()
        
        if not plant:
            return None

        # Get plant measurements
        measurements_result = await session.execute(
            select(Measurement).where(Measurement.plant_id == plant.id)
        )
        measurements = measurements_result.scalars().all()

        # Get plant activities
        activities_result = await session.execute(
            select(PlantActivity).where(PlantActivity.plant_id == plant.id)
        )
        activities = activities_result.scalars().all()

        # Get plant status history
        status_history_result = await session.execute(
            select(Status).where(Status.plant_id == plant.id)
        )
        status_history = status_history_result.scalars().all()

        # Get plant images
        images_result = await session.execute(
            select(PlantImage)
            .where(PlantImage.plant_id == plant.id)
            .order_by(desc(PlantImage.image_date))
        )
        images = images_result.scalars().all()

        # Get latest image
        latest_image = images[0] if images else None

        # Calculate days since last watering and feeding
        days_since_watering = calculate_days_since(plant.last_water_date)
        days_since_feeding = calculate_days_since(plant.last_feed_date)

        # Calculate current day and week
        current_day = calculate_days_since(plant.start_dt)
        current_week = calculate_weeks_since(plant.start_dt)

        # Calculate estimated harvest date
        est_harvest_date = estimate_harvest_date(
            plant.start_dt, plant.cycle_time, plant.autoflower
        )

        # Build plant data
        plant_data = {
            "id": plant.id,
            "name": plant.name,
            "description": plant.description,
            "status": plant.status_name,
            "status_id": plant.status_id,
            "strain_name": plant.cultivar_name,  # Fix: use cultivar_name
            "strain_id": plant.cultivar_id,  # Fix: use cultivar_id
            "breeder_name": plant.breeder_name,
            "zone_name": plant.zone_name,
            "zone_id": plant.zone_id,
            "current_day": current_day,
            "current_week": current_week,
            "current_height": plant.current_height,
            "height_date": plant.height_date,
            "last_water_date": plant.last_water_date,
            "last_feed_date": plant.last_feed_date,
            "days_since_watering": days_since_watering,
            "days_since_feeding": days_since_feeding,
            "measurements": [
                {"id": m.id, "name": m.name, "value": m.value, "date": m.date}
                for m in measurements
            ],
            "activities": [
                {
                    "id": a.id,
                    "name": a.activity_name,
                    "note": a.note,
                    "date": a.date,
                    "activity_id": None,
                }
                for a in activities
            ],
            "status_history": [
                {"id": s.id, "status": s.status, "date": s.date} for s in status_history
            ],
            "latest_image": (
                {
                    "id": latest_image.id,
                    "image_path": latest_image.image_path,
                    "image_description": latest_image.image_description,
                    "image_date": latest_image.image_date,
                }
                if latest_image
                else None
            ),
            "images": [
                {
                    "id": img.id,
                    "image_path": img.image_path,
                    "image_description": img.image_description,
                    "image_date": img.image_date,
                }
                for img in images
            ],
            "is_clone": plant.is_clone,
            "start_dt": plant.start_dt,
            "harvest_weight": plant.harvest_weight,
            "harvest_date": plant.harvest_date,
            "cycle_time": plant.cycle_time,
            "strain_url": plant.cultivar_url,  # Fix: use cultivar_url
            "est_harvest_date": est_harvest_date,
            "autoflower": plant.autoflower,
            "parent_id": plant.parent_id,
            "parent_name": plant.parent_name,
        }

        return plant_data
    except Exception as e:
        logger.error(f"Error getting plant: {e}")
        return None


async def get_living_plants(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all living plants - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: The living plants.
    """
    try:
        # Get plants with status other than 'Harvested' (4) or 'Dead' (5)
        plants_result = await session.execute(
            select(Plant).where(Plant.status_id.notin_([4, 5]))
        )
        plants = plants_result.scalars().all()

        plant_list = []
        for plant in plants:
            # Calculate days since last watering and feeding
            days_since_watering = calculate_days_since(plant.last_water_date)
            days_since_feeding = calculate_days_since(plant.last_feed_date)

            # Calculate current day and week
            current_day = calculate_days_since(plant.start_dt)
            current_week = calculate_weeks_since(plant.start_dt)

            # Calculate flowering days if the plant is in flowering stage
            flowering_days = None
            if plant.status_id == 3:  # Flowering
                flowering_status_result = await session.execute(
                    select(Status).where(
                        and_(
                            Status.plant_id == plant.id,
                            Status.status == "Flowering"
                        )
                    )
                )
                flowering_status = flowering_status_result.scalars().first()
                if flowering_status:
                    flowering_days = calculate_days_since(flowering_status.date)

            # Calculate estimated harvest date
            est_harvest_date = estimate_harvest_date(
                plant.start_dt, plant.cycle_time, plant.autoflower
            )

            # Get the latest status date
            latest_status_result = await session.execute(
                select(Status)
                .where(Status.plant_id == plant.id)
                .order_by(desc(Status.date))
                .limit(1)
            )
            latest_status = latest_status_result.scalars().first()
            status_date = latest_status.date if latest_status else plant.start_dt

            plant_data = {
                "id": plant.id,
                "name": plant.name,
                "description": plant.description,
                "clone": plant.is_clone,
                "strain_name": plant.strain_name,
                "breeder_name": plant.breeder_name,
                "zone_name": plant.zone_name,
                "start_dt": (
                    plant.start_dt.strftime("%Y-%m-%d") if plant.start_dt else None
                ),
                "current_week": current_week,
                "current_day": current_day,
                "days_since_last_watering": days_since_watering,
                "days_since_last_feeding": days_since_feeding,
                "flowering_days": flowering_days,
                "harvest_weight": plant.harvest_weight,
                "status": plant.status_name,
                "status_date": status_date,
                "cycle_time": plant.cycle_time,
                "strain_url": plant.strain_url,
                "est_harvest_date": est_harvest_date,
                "autoflower": plant.autoflower,
            }

            plant_list.append(plant_data)

        return plant_list
    except Exception as e:
        logger.error(f"Error getting living plants: {e}")
        return []


async def get_harvested_plants(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all harvested plants - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: The harvested plants.
    """
    try:
        plants_result = await session.execute(
            select(Plant).where(Plant.status_id == 4)
        )
        plants = plants_result.scalars().all()

        plant_list = []
        for plant in plants:
            # Calculate cycle time
            cycle_time = None
            if plant.start_dt and plant.harvest_date:
                delta = plant.harvest_date - plant.start_dt
                cycle_time = delta.days

            # Get the latest status date
            latest_status_result = await session.execute(
                select(Status)
                .where(Status.plant_id == plant.id)
                .order_by(desc(Status.date))
                .limit(1)
            )
            latest_status = latest_status_result.scalars().first()
            status_date = latest_status.date if latest_status else plant.start_dt

            plant_data = {
                "id": plant.id,
                "name": plant.name,
                "description": plant.description,
                "clone": plant.is_clone,
                "strain_name": plant.strain_name,
                "breeder_name": plant.breeder_name,
                "zone_name": plant.zone_name,
                "start_dt": (
                    plant.start_dt.strftime("%Y-%m-%d") if plant.start_dt else None
                ),
                "harvest_weight": plant.harvest_weight,
                "status": plant.status_name,
                "status_date": status_date,
                "cycle_time": cycle_time,
                "strain_url": plant.strain_url,
                "harvest_date": plant.harvest_date,
                "autoflower": plant.autoflower,
            }

            plant_list.append(plant_data)

        return plant_list
    except Exception as e:
        logger.error(f"Error getting harvested plants: {e}")
        return []


async def get_dead_plants(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all dead plants - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: The dead plants.
    """
    try:
        plants_result = await session.execute(
            select(Plant).where(Plant.status_id == 5)
        )
        plants = plants_result.scalars().all()

        plant_list = []
        for plant in plants:
            # Calculate cycle time
            cycle_time = None
            if plant.start_dt:
                latest_status_result = await session.execute(
                    select(Status)
                    .where(Status.plant_id == plant.id)
                    .order_by(desc(Status.date))
                    .limit(1)
                )
                latest_status = latest_status_result.scalars().first()
                if latest_status:
                    delta = latest_status.date - plant.start_dt
                    cycle_time = delta.days

            # Get the latest status date
            latest_status_result = await session.execute(
                select(Status)
                .where(Status.plant_id == plant.id)
                .order_by(desc(Status.date))
                .limit(1)
            )
            latest_status = latest_status_result.scalars().first()
            status_date = latest_status.date if latest_status else plant.start_dt

            plant_data = {
                "id": plant.id,
                "name": plant.name,
                "description": plant.description,
                "clone": plant.is_clone,
                "strain_name": plant.strain_name,
                "breeder_name": plant.breeder_name,
                "zone_name": plant.zone_name,
                "start_dt": (
                    plant.start_dt.strftime("%Y-%m-%d") if plant.start_dt else None
                ),
                "status": plant.status_name,
                "status_date": status_date,
                "cycle_time": cycle_time,
                "strain_url": plant.strain_url,
                "autoflower": plant.autoflower,
            }

            plant_list.append(plant_data)

        return plant_list
    except Exception as e:
        logger.error(f"Error getting dead plants: {e}")
        return []


async def add_plant(data: Dict[str, Any], session: AsyncSession, user_id: int = None) -> Dict[str, Any]:
    """
    Add a new plant - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): The plant data.
        session: AsyncSession for database operations
        user_id (int): The ID of the user adding the plant

    Returns:
        Dict[str, Any]: The result of the operation with success status and plant ID.
    """
    try:
        # Set default status to 'Seedling' (status_id=1) if not provided
        status_id = data.get("status_id", 1)

        # Create a new plant
        plant = Plant(
            name=data.get("name"),
            description=data.get("description", ""),
            status_id=status_id,
            strain_id=data.get("strain_id"),
            zone_id=data.get("zone_id"),
            is_clone=data.get("is_clone", False),
            start_dt=datetime.now(),
            autoflower=data.get("autoflower", False),
            parent_id=data.get("parent_id"),
        )

        # Add the plant to the database
        session.add(plant)
        await session.commit()
        await session.refresh(plant)

        # Get the status name from the database
        status_result = await session.execute(
            select(Status).where(Status.id == status_id)
        )
        status_obj = status_result.scalars().first()
        status_name = "Seedling" if not status_obj else status_obj.status

        # Add the initial status history entry
        status_history = Status(
            plant_id=plant.id, status=status_name, date=datetime.now()
        )

        session.add(status_history)
        await session.commit()

        # Log system activity if user_id provided
        if user_id:
            activity = SystemActivity(
                user_id=user_id,
                type="plant_created",
                details=f"Plant created: {plant.name}",
                timestamp=datetime.now(),
            )
            session.add(activity)
            await session.commit()

        # Return success with the plant ID
        return {"success": True, "id": plant.id}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error adding plant: {e}")
        return {"success": False, "error": str(e)}


async def update_plant(data: Dict[str, Any], session: AsyncSession, user_id: int = None) -> Dict[str, Any]:
    """
    Update a plant - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): The plant data.
        session: AsyncSession for database operations
        user_id (int): The ID of the user updating the plant

    Returns:
        Dict[str, Any]: The result of the operation.
    """
    try:
        plant_id = data.get("id")
        plant_result = await session.execute(select(Plant).where(Plant.id == plant_id))
        plant = plant_result.scalars().first()

        if not plant:
            return {"success": False, "error": "Plant not found"}

        # Update plant fields
        plant.name = data.get("name", plant.name)
        plant.description = data.get("description", plant.description)

        # Check if status has changed
        new_status_id = data.get("status_id")
        if new_status_id and new_status_id != plant.status_id:
            plant.status_id = new_status_id

            # Get the new status name
            status_result = await session.execute(
                select(Status).where(Status.id == new_status_id)
            )
            status_obj = status_result.scalars().first()
            status_name = status_obj.status if status_obj else "Unknown"

            # Add a new status history entry
            status = Status(
                plant_id=plant.id, status=status_name, date=datetime.now()
            )

            session.add(status)

            # If the plant is harvested, set the harvest date
            if new_status_id == 4:  # Harvested
                plant.harvest_date = datetime.now()

                # Calculate cycle time
                if plant.start_dt:
                    delta = datetime.now() - plant.start_dt
                    plant.cycle_time = delta.days

        # Update other fields
        plant.strain_id = data.get("strain_id", plant.strain_id)
        plant.zone_id = data.get("zone_id", plant.zone_id)
        plant.current_height = data.get("current_height", plant.current_height)
        plant.height_date = (
            datetime.now() if data.get("current_height") else plant.height_date
        )
        plant.harvest_weight = data.get("harvest_weight", plant.harvest_weight)
        plant.strain_url = data.get("strain_url", plant.strain_url)
        plant.autoflower = data.get("autoflower", plant.autoflower)

        # Update watering and feeding dates
        if data.get("watered"):
            plant.last_water_date = datetime.now()

            # Add a watering activity
            activity = PlantActivity(
                plant_id=plant.id,
                name="Water",
                note=data.get("water_note", ""),
                date=datetime.now(),
                activity_id=1,  # Water activity ID
            )

            session.add(activity)

        if data.get("fed"):
            plant.last_feed_date = datetime.now()

            # Add a feeding activity
            activity = PlantActivity(
                plant_id=plant.id,
                name="Feed",
                note=data.get("feed_note", ""),
                date=datetime.now(),
                activity_id=2,  # Feed activity ID
            )

            session.add(activity)

        await session.commit()

        # Log system activity if user_id provided
        if user_id:
            activity = SystemActivity(
                user_id=user_id,
                type="plant_updated",
                details=f"Plant updated: {plant.name}",
                timestamp=datetime.now(),
            )
            session.add(activity)
            await session.commit()

        return {"success": True, "plant_id": plant.id}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating plant: {e}")
        return {"success": False, "error": str(e)}


async def delete_plant(plant_id: int, session: AsyncSession, user_id: int = None, app_root_path: str = None) -> Dict[str, Any]:
    """
    Delete a plant - ASYNC VERSION.

    Args:
        plant_id (int): The ID of the plant.
        session: AsyncSession for database operations
        user_id (int): The ID of the user deleting the plant

    Returns:
        Dict[str, Any]: The result of the operation.
    """
    try:
        plant_result = await session.execute(select(Plant).where(Plant.id == plant_id))
        plant = plant_result.scalars().first()

        if not plant:
            return {"success": False, "error": "Plant not found"}

        plant_name = plant.name

        # Delete plant images
        images_result = await session.execute(
            select(PlantImage).where(PlantImage.plant_id == plant.id)
        )
        images = images_result.scalars().all()
        for image in images:
            # Delete the image file
            image_path = os.path.join(app_root_path or "", image.image_path)
            if os.path.exists(image_path):
                os.remove(image_path)

            await session.delete(image)

        # Delete plant activities
        activities_result = await session.execute(
            select(PlantActivity).where(PlantActivity.plant_id == plant.id)
        )
        activities = activities_result.scalars().all()
        for activity in activities:
            await session.delete(activity)

        # Delete plant measurements
        measurements_result = await session.execute(
            select(Measurement).where(Measurement.plant_id == plant.id)
        )
        measurements = measurements_result.scalars().all()
        for measurement in measurements:
            await session.delete(measurement)

        # Delete plant status history
        statuses_result = await session.execute(
            select(Status).where(Status.plant_id == plant.id)
        )
        statuses = statuses_result.scalars().all()
        for status in statuses:
            await session.delete(status)

        # Delete the plant
        await session.delete(plant)
        await session.commit()

        # Log system activity if user_id provided
        if user_id:
            activity = SystemActivity(
                user_id=user_id,
                type="plant_deleted",
                details=f"Plant deleted: {plant_name}",
                timestamp=datetime.now(),
            )
            session.add(activity)
            await session.commit()

        return {"success": True}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting plant: {e}")
        return {"success": False, "error": str(e)}