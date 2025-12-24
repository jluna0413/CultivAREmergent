"""
Async data export handlers for the CultivAR application.
"""

import csv
import json
import os
import zipfile
from datetime import datetime, timezone
from io import BytesIO, StringIO
from typing import List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.logger import logger
from app.models_async.grow import Plant, Cultivar
from app.models_async.sensors import Sensor, SensorData
from app.models_async.auth import User # Corrected import for User
from app.models_async.activities import ActivityLog, ActivityType, PlantActivity # Updated imports

# Import async versions of other handlers
# from .plant_handlers import get_living_plants, get_harvested_plants, get_dead_plants
from .strain_handlers import get_cultivars_async # Updated import
# from .user_handlers import get_all_users
from .sensor_handlers import get_sensors


async def export_plants_csv(session: AsyncSession) -> str:
    """
    Export all plants to CSV format.
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        header = [
            "ID", "Name", "Description", "Status", "Strain", "Breeder", "Zone",
            "Is Clone", "Start Date", "Current Week", "Current Day", "Current Height",
            "Last Water Date", "Last Feed Date", "Harvest Weight", "Harvest Date",
            "Cycle Time", "Autoflower", "Parent Plant",
        ]
        writer.writerow(header)

        living_plants = await get_living_plants(session)
        harvested_plants = await get_harvested_plants(session)
        dead_plants = await get_dead_plants(session)

        all_plants = living_plants + harvested_plants + dead_plants

        for plant in all_plants:
            row = [
                plant.get("id", ""),
                plant.get("name", ""),
                plant.get("description", ""),
                plant.get("status", ""),
                plant.get("strain_name", ""),
                plant.get("breeder_name", ""),
                plant.get("zone_name", ""),
                "Yes" if plant.get("clone", False) else "No",
                plant.get("start_dt", ""),
                plant.get("current_week", ""),
                plant.get("current_day", ""),
                plant.get("current_height", ""),
                plant.get("last_water_date", ""),
                plant.get("last_feed_date", ""),
                plant.get("harvest_weight", ""),
                plant.get("harvest_date", ""),
                plant.get("cycle_time", ""),
                "Yes" if plant.get("autoflower", False) else "No",
                plant.get("parent_name", ""),
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting plants to CSV: {e}")
        return ""


async def export_strains_csv(session: AsyncSession) -> str:
    """
    Export all strains to CSV format.
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        header = [
            "ID", "Name", "Breeder", "Indica %", "Sativa %", "Autoflower",
            "Description", "Seed Count", "Cycle Time", "URL", "Parent 1", "Parent 2",
            "Lineage JSON", "SeedFinder ID", "THC Content", "CBD Content", "Flowering Type",
            "Categories",
        ]
        writer.writerow(header)

        all_cultivars = await get_cultivars_async(session, in_stock=False) # Get all, regardless of stock

        for cultivar in all_cultivars:
            row = [
                cultivar.get("id", ""),
                cultivar.get("name", ""),
                cultivar.get("breeder", ""),
                cultivar.get("indica", ""),
                cultivar.get("sativa", ""),
                "Yes" if cultivar.get("autoflower", False) else "No",
                cultivar.get("description", ""),
                cultivar.get("seed_count", ""),
                cultivar.get("cycle_time", ""),
                cultivar.get("url", ""),
                cultivar.get("parent_1", ""),
                cultivar.get("parent_2", ""),
                json.dumps(cultivar.get("lineage_json", {})) if cultivar.get("lineage_json") else "",
                cultivar.get("seedfinder_id", ""),
                cultivar.get("thc_content", ""),
                cultivar.get("cbd_content", ""),
                cultivar.get("flowering_type", ""),
                json.dumps(cultivar.get("categories", [])) if cultivar.get("categories") else "",
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting strains to CSV: {e}")
        return ""


async def export_activities_csv(session: AsyncSession) -> str:
    """
    Export all plant activities to CSV format.
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        header = [
            "Activity ID", "Plant ID", "Plant Name", "Activity Type",
            "Activity Name", "Note", "Date", "User ID", "Username", "IP Address",
        ]
        writer.writerow(header)

        stmt = select(PlantActivity).options(selectinload(PlantActivity.plant), selectinload(PlantActivity.activity_type_rel))
        result = await session.execute(stmt)
        activities = result.scalars().all()

        for activity in activities:
            row = [
                activity.id,
                activity.plant_id,
                activity.plant.name if activity.plant else "",
                activity.activity_type_rel.name if activity.activity_type_rel else "", # Updated
                activity.activity_name,
                activity.note or "",
                activity.date.strftime("%Y-%m-%d %H:%M:%S") if activity.date else "",
                activity.user_id,
                activity.username,
                activity.ip_address,
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting activities to CSV: {e}")
        return ""


async def export_users_csv(session: AsyncSession) -> str:
    """
    Export all users to CSV format.
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        header = [
            "ID", "Username", "Phone", "Email", "Is Admin",
            "Force Password Change", "Created At", "Updated At",
            "User Type", "Tier", "Is Verified Breeder",
        ]
        writer.writerow(header)

        users = await get_all_users(session)

        for user in users:
            row = [
                user.get("id", ""),
                user.get("username", ""),
                user.get("phone", ""),
                user.get("email", ""),
                "Yes" if user.get("is_admin", False) else "No",
                "Yes" if user.get("force_password_change", False) else "No",
                user.get("created_at", ""),
                user.get("updated_at", ""),
                user.get("user_type", ""),
                user.get("tier", ""),
                "Yes" if user.get("is_verified_breeder", False) else "No",
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting users to CSV: {e}")
        return ""


async def export_plants_json(session: AsyncSession) -> str:
    """
    Export all plants to JSON format.
    """
    try:
        living_plants = await get_living_plants(session)
        harvested_plants = await get_harvested_plants(session)
        dead_plants = await get_dead_plants(session)

        export_data = {
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "export_type": "plants",
            "living_plants": living_plants,
            "harvested_plants": harvested_plants,
            "dead_plants": dead_plants,
            "total_plants": len(living_plants) + len(harvested_plants) + len(dead_plants),
        }

        return json.dumps(export_data, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error exporting plants to JSON: {e}")
        return ""


async def export_strains_json(session: AsyncSession) -> str:
    """
    Export all strains to JSON format.
    """
    try:
        all_cultivars = await get_cultivars_async(session, in_stock=False) # Get all, regardless of stock

        export_data = {
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "export_type": "strains",
            "cultivars": all_cultivars,
            "total_cultivars": len(all_cultivars),
        }

        return json.dumps(export_data, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error exporting strains to JSON: {e}")
        return ""


async def export_sensors_csv(session: AsyncSession) -> str:
    """
    Export sensor data to CSV format.
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        header = [
            "Sensor ID", "Sensor Name", "Zone", "Source", "Device", "Type", "Unit",
            "Latest Reading", "Latest Reading Date", "Location",
        ]
        writer.writerow(header)

        sensors = await get_sensors(session)

        for sensor in sensors:
            row = [
                sensor.get("id", ""),
                sensor.get("name", ""),
                sensor.get("zone", ""),
                sensor.get("source", ""),
                sensor.get("device", ""),
                sensor.get("type", ""),
                sensor.get("unit", ""),
                sensor.get("latest_reading", {}).get("value", ""),
                sensor.get("latest_reading", {}).get("date", ""),
                sensor.get("location", ""),
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting sensors to CSV: {e}")
        return ""


async def export_complete_backup(session: AsyncSession) -> BytesIO:
    """
    Create a complete backup of all application data in ZIP format.
    """
    try:
        zip_buffer = BytesIO()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file: # Removed async with
            plants_csv = await export_plants_csv(session)
            if plants_csv:
                zip_file.writestr(f"plants_{timestamp}.csv", plants_csv)

            plants_json = await export_plants_json(session)
            if plants_json:
                zip_file.writestr(f"plants_{timestamp}.json", plants_json)

            strains_csv = await export_strains_csv(session)
            if strains_csv:
                zip_file.writestr(f"strains_{timestamp}.csv", strains_csv)

            strains_json = await export_strains_json(session)
            if strains_json:
                zip_file.writestr(f"strains_{timestamp}.json", strains_json)

            activities_csv = await export_activities_csv(session)
            if activities_csv:
                zip_file.writestr(f"activities_{timestamp}.csv", activities_csv)

            users_csv = await export_users_csv(session)
            if users_csv:
                zip_file.writestr(f"users_{timestamp}.csv", users_csv)

            sensors_csv = await export_sensors_csv(session)
            if sensors_csv:
                zip_file.writestr(f"sensors_{timestamp}.csv", sensors_csv)

            metadata = {
                "backup_timestamp": datetime.now(timezone.utc).isoformat(),
                "application": "CultivAR",
                "version": "1.0.0",
                "backup_type": "complete",
                "files_included": [
                    f"plants_{timestamp}.csv",
                    f"plants_{timestamp}.json",
                    f"strains_{timestamp}.csv",
                    f"strains_{timestamp}.json",
                    f"activities_{timestamp}.csv",
                    f"users_{timestamp}.csv",
                    f"sensors_{timestamp}.csv",
                ],
            }
            zip_file.writestr("backup_metadata.json", json.dumps(metadata, indent=2))

        zip_buffer.seek(0)
        return zip_buffer
    except Exception as e:
        logger.error(f"Error creating complete backup: {e}")
        return BytesIO()


async def get_export_statistics(session: AsyncSession) -> Dict[str, Any]:
    """
    Get statistics about exportable data.
    """
    try:
        total_plants = (await session.execute(select(func.count(Plant.id)))).scalar_one()
        living_plants = (await session.execute(select(func.count(Plant.id)).where(Plant.status_id.notin_([4, 5])))).scalar_one()
        harvested_plants = (await session.execute(select(func.count(Plant.id)).where(Plant.status_id == 4))).scalar_one()
        dead_plants = (await session.execute(select(func.count(Plant.id)).where(Plant.status_id == 5))).scalar_one()
        total_strains = (await session.execute(select(func.count(Cultivar.id)))).scalar_one()
        in_stock_strains = (await session.execute(select(func.count(Cultivar.id)).where(Cultivar.seed_count > 0))).scalar_one()
        out_of_stock_strains = (await session.execute(select(func.count(Cultivar.id)).where(Cultivar.seed_count == 0))).scalar_one()
        total_activities = (await session.execute(select(func.count(PlantActivity.id)))).scalar_one() # Updated to PlantActivity
        total_users = (await session.execute(select(func.count(User.id)))).scalar_one()
        total_sensors = (await session.execute(select(func.count(Sensor.id)))).scalar_one()
        total_sensor_readings = (await session.execute(select(func.count(SensorData.id)))).scalar_one()

        stats = {
            "total_plants": total_plants,
            "living_plants": living_plants,
            "harvested_plants": harvested_plants,
            "dead_plants": dead_plants,
            "total_strains": total_strains,
            "in_stock_strains": in_stock_strains,
            "out_of_stock_strains": out_of_stock_strains,
            "total_activities": total_activities,
            "total_users": total_users,
            "total_sensors": total_sensors,
            "total_sensor_readings": total_sensor_readings,
            "last_export_date": "Never",  # This could be stored in settings
        }
        return stats
    except Exception as e:
        logger.error(f"Error getting export statistics: {e}")
        return {
            "total_plants": 0, "living_plants": 0, "harvested_plants": 0, "dead_plants": 0,
            "total_strains": 0, "in_stock_strains": 0, "out_of_stock_strains": 0,
            "total_activities": 0, "total_users": 0, "total_sensors": 0,
            "total_sensor_readings": 0, "last_export_date": "Never",
        }
