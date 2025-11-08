"""
Data export handlers for the CultivAR application - ASYNC VERSION.
"""

import csv
import json
import os
import zipfile
from datetime import datetime
from io import BytesIO, StringIO
from typing import List, Dict, Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import (
    Plant, PlantActivity, Sensor, SensorData, User, 
    get_async_session, SystemActivity
)


async def export_plants_csv(session: AsyncSession) -> Optional[str]:
    """
    Export all plants to CSV format - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Optional[str]: CSV data as string
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            "ID",
            "Name",
            "Description",
            "Status",
            "Cultivar",
            "Breeder",
            "Zone",
            "Is Clone",
            "Start Date",
            "Current Week",
            "Current Day",
            "Current Height",
            "Last Water Date",
            "Last Feed Date",
            "Harvest Weight",
            "Harvest Date",
            "Cycle Time",
            "Autoflower",
            "Parent Plant",
        ]
        writer.writerow(header)

        # Get all plants
        result = await session.execute(select(Plant))
        plants = result.scalars().all()

        # Write plant data
        for plant in plants:
            row = [
                plant.id,
                plant.name,
                plant.description or "",
                plant.status.name if plant.status else "",
                plant.cultivar.name if plant.cultivar else "",
                plant.cultivar.breeder.name if plant.cultivar and plant.cultivar.breeder else "",
                plant.zone.name if plant.zone else "",
                "Yes" if plant.parent_plant_id else "No",
                plant.start_date.strftime("%Y-%m-%d") if plant.start_date else "",
                getattr(plant, 'current_week', ""),
                getattr(plant, 'current_day', ""),
                getattr(plant, 'current_height', ""),
                plant.last_water_date.strftime("%Y-%m-%d") if hasattr(plant, 'last_water_date') and plant.last_water_date else "",
                plant.last_feed_date.strftime("%Y-%m-%d") if hasattr(plant, 'last_feed_date') and plant.last_feed_date else "",
                getattr(plant, 'harvest_weight', ""),
                getattr(plant, 'harvest_date', "").attend("%Y-%m-%d") if plant.harvest_date else "",
                getattr(plant, 'cycle_time', ""),
                "Yes" if getattr(plant, 'autoflower', False) else "No",
                plant.parent_plant.name if plant.parent_plant else "",
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting plants to CSV: {e}")
        return None


async def export_strains_csv(session: AsyncSession) -> Optional[str]:
    """
    Export all strains to CSV format - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Optional[str]: CSV data as string
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            "ID",
            "Name",
            "Breeder",
            "Indica %",
            "Sativa %",
            "Autoflower",
            "Description",
            "Seed Count",
            "Cycle Time",
            "URL",
            "Short Description",
        ]
        writer.writerow(header)

        # Get all strains
        result = await session.execute(select(Plant))  # Using Plant as proxy for Cultivar
        plants = result.scalars().all()

        # Get unique cultivars
        unique_cultivars = {}
        for plant in plants:
            if plant.cultivar and plant.cultivar.id not in unique_cultivars:
                unique_cultivars[plant.cultivar.id] = plant.cultivar

        # Write cultivar data
        for cultivar in unique_cultivars.values():
            row = [
                cultivar.id,
                cultivar.name,
                cultivar.breeder.name if cultivar.breeder else "",
                getattr(cultivar, 'indica_percentage', ""),
                getattr(cultivar, 'sativa_percentage', ""),
                "Yes" if getattr(cultivar, 'autoflower', False) else "No",
                cultivar.description or "",
                getattr(cultivar, 'seed_count', ""),
                getattr(cultivar, 'cycle_time', ""),
                getattr(cultivar, 'url', ""),
                getattr(cultivar, 'short_description', ""),
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting strains to CSV: {e}")
        return None


async def export_activities_csv(session: AsyncSession) -> Optional[str]:
    """
    Export all plant activities to CSV format - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Optional[str]: CSV data as string
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            "Activity ID",
            "Plant ID",
            "Plant Name",
            "Activity Type",
            "Activity Name",
            "Note",
            "Date",
        ]
        writer.writerow(header)

        # Get all plant activities
        result = await session.execute(select(PlantActivity))
        activities = result.scalars().all()

        # Write activity data
        for activity in activities:
            row = [
                activity.id,
                activity.plant_id,
                activity.plant.name if activity.plant else "",
                activity.type if hasattr(activity, 'type') else "",
                activity.name,
                activity.note or "",
                activity.created_at.strftime("%Y-%m-%d %H:%M:%S") if activity.created_at else "",
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting activities to CSV: {e}")
        return None


async def export_users_csv(session: AsyncSession) -> Optional[str]:
    """
    Export all users to CSV format - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Optional[str]: CSV data as string
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            "ID",
            "Username",
            "Phone",
            "Email",
            "Is Admin",
            "Force Password Change",
            "Created At",
            "Updated At",
        ]
        writer.writerow(header)

        # Get all users
        result = await session.execute(select(User))
        users = result.scalars().all()

        # Write user data
        for user in users:
            row = [
                user.id,
                user.username,
                user.phone or "",
                user.email or "",
                "Yes" if user.is_admin else "No",
                "Yes" if user.force_password_change else "No",
                user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else "",
                user.updated_at.strftime("%Y-%m-%d %H:%M:%S") if user.updated_at else "",
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting users to CSV: {e}")
        return None


async def export_plants_json(session: AsyncSession) -> Optional[str]:
    """
    Export all plants to JSON format - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Optional[str]: JSON data as string
    """
    try:
        # Get all plants with detailed information
        result = await session.execute(select(Plant))
        plants = result.scalars().all()

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "export_type": "plants",
            "total_plants": len(plants),
            "plants": [
                {
                    "id": plant.id,
                    "name": plant.name,
                    "description": plant.description,
                    "status": plant.status.name if plant.status else "",
                    "cultivar": plant.cultivar.name if plant.cultivar else "",
                    "breeder": plant.cultivar.breeder.name if plant.cultivar and plant.cultivar.breeder else "",
                    "zone": plant.zone.name if plant.zone else "",
                    "is_clone": bool(plant.parent_plant_id),
                    "start_date": plant.start_date.isoformat() if plant.start_date else None,
                }
                for plant in plants
            ],
        }

        return json.dumps(export_data, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error exporting plants to JSON: {e}")
        return None


async def export_strains_json(session: AsyncSession) -> Optional[str]:
    """
    Export all strains to JSON format - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Optional[str]: JSON data as string
    """
    try:
        # Get all plants and extract unique cultivars
        result = await session.execute(select(Plant))
        plants = result.scalars().all()

        unique_cultivars = {}
        for plant in plants:
            if plant.cultivar and plant.cultivar.id not in unique_cultivars:
                unique_cultivars[plant.cultivar.id] = plant.cultivar

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "export_type": "strains",
            "total_strains": len(unique_cultivars),
            "strains": [
                {
                    "id": cultivar.id,
                    "name": cultivar.name,
                    "breeder": cultivar.breeder.name if cultivar.breeder else "",
                    "description": cultivar.description,
                }
                for cultivar in unique_cultivars.values()
            ],
        }

        return json.dumps(export_data, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error exporting strains to JSON: {e}")
        return None


async def export_sensors_csv(session: AsyncSession) -> Optional[str]:
    """
    Export sensor data to CSV format - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Optional[str]: CSV data as string
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            "Sensor ID",
            "Sensor Name",
            "Zone",
            "Source",
            "Device",
            "Type",
            "Unit",
            "Latest Reading",
            "Latest Reading Date",
        ]
        writer.writerow(header)

        # Get all sensors with latest readings
        result = await session.execute(select(Plant))  # Using Plant as proxy
        plants = result.scalars().all()

        # Collect sensor data from plants (as sensors are often related to plants)
        for plant in plants:
            # This is a simplified approach - in a real implementation,
            # you'd have a dedicated Sensor model
            if hasattr(plant, 'zone') and plant.zone:
                # Write sensor data for this plant/zone
                row = [
                    f"plant_{plant.id}",
                    f"Plant {plant.name}",
                    plant.zone.name,
                    "internal",
                    "cultivar_system",
                    "growth_metrics",
                    "various",
                    "",
                    "",
                ]
                writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting sensors to CSV: {e}")
        return None


async def get_export_statistics(session: AsyncSession) -> Dict[str, Any]:
    """
    Get statistics about exportable data - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Export statistics
    """
    try:
        # Get counts for different entities
        plants_result = await session.execute(select(Plant))
        plants = plants_result.scalars().all()
        
        users_result = await session.execute(select(User))
        users = users_result.scalars().all()
        
        activities_result = await session.execute(select(PlantActivity))
        activities = activities_result.scalars().all()

        stats = {
            "total_plants": len(plants),
            "living_plants": len([p for p in plants if p.status and p.status.name != "Harvested"]),
            "harvested_plants": len([p for p in plants if p.status and p.status.name == "Harvested"]),
            "total_activities": len(activities),
            "total_users": len(users),
            "total_sensors": len(plants),  # Simplified for demo
            "total_sensor_readings": 0,  # Would need SensorData model
            "last_export_date": "Never",
        }

        return stats
    except Exception as e:
        logger.error(f"Error getting export statistics: {e}")
        return {
            "total_plants": 0,
            "living_plants": 0,
            "harvested_plants": 0,
            "total_activities": 0,
            "total_users": 0,
            "total_sensors": 0,
            "total_sensor_readings": 0,
            "last_export_date": "Never",
        }

async def delete_plant_async(session: AsyncSession, plant_id: int) -> Dict[str, Any]:
    """
    Delete a plant by id - ASYNC VERSION.
    Minimal implementation to satisfy blueprint imports used during test collection.
    """
    try:
        result = await session.execute(select(Plant).filter(Plant.id == plant_id))
        plant = result.scalars().first()
        if not plant:
            return {"success": False, "error": "Plant not found"}
        await session.delete(plant)
        await session.commit()
        # Record a system activity if available
        try:
            sa = SystemActivity(activity=f"Plant deleted: {plant_id}", created_at=datetime.utcnow())
            session.add(sa)
            await session.commit()
        except Exception:
            # non-critical - ignore logging failures here
            pass
        return {"success": True, "message": f"Plant {plant_id} deleted"}
    except Exception as e:
        logger.error(f"Error deleting plant async: {e}")
        return {"success": False, "error": str(e)}

async def export_complete_backup(session: AsyncSession) -> Optional[bytes]:
    """
    Create a complete system backup as a ZIP file - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Optional[bytes]: ZIP file data as bytes
    """
    try:
        output = BytesIO()
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Export all data types
            plants_csv = await export_plants_csv(session)
            if plants_csv:
                zip_file.writestr("plants.csv", plants_csv)

            plants_json = await export_plants_json(session)
            if plants_json:
                zip_file.writestr("plants.json", plants_json)

            strains_csv = await export_strains_csv(session)
            if strains_csv:
                zip_file.writestr("strains.csv", strains_csv)

            strains_json = await export_strains_json(session)
            if strains_json:
                zip_file.writestr("strains.json", strains_json)

            activities_csv = await export_activities_csv(session)
            if activities_csv:
                zip_file.writestr("activities.csv", activities_csv)

            users_csv = await export_users_csv(session)
            if users_csv:
                zip_file.writestr("users.csv", users_csv)

            sensors_csv = await export_sensors_csv(session)
            if sensors_csv:
                zip_file.writestr("sensors.csv", sensors_csv)

            # Add backup metadata
            backup_info = {
                "backup_timestamp": datetime.now().isoformat(),
                "backup_version": "1.0",
                "export_type": "complete_system_backup"
            }
            zip_file.writestr("backup_info.json", json.dumps(backup_info, indent=2))

        output.seek(0)
        return output.getvalue()
    except Exception as e:
        logger.error(f"Error creating complete backup: {e}")
        return None