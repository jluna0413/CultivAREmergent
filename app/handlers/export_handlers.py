"""
Data export handlers for the CultivAR application.
"""

import csv
import json
import os
import zipfile
from datetime import datetime
from io import BytesIO, StringIO

from app.handlers.plant_handlers import (
    get_dead_plants,
    get_harvested_plants,
    get_living_plants,
)
from app.handlers.strain_handlers import get_in_stock_strains, get_out_of_stock_strains
from app.handlers.user_handlers import get_all_users
from app.logger import logger
from app.models.base_models import (
    Plant,
    PlantActivity,
    Sensor,
    SensorData,
    Strain,
    User,
)


def export_plants_csv():
    """
    Export all plants to CSV format.

    Returns:
        str: CSV data as string
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
            "Strain",
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
        living_plants = get_living_plants()
        harvested_plants = get_harvested_plants()
        dead_plants = get_dead_plants()

        all_plants = living_plants + harvested_plants + dead_plants

        # Write plant data
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
        return None


def export_strains_csv():
    """
    Export all strains to CSV format.

    Returns:
        str: CSV data as string
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
        in_stock_strains = get_in_stock_strains()
        out_of_stock_strains = get_out_of_stock_strains()

        all_strains = in_stock_strains + out_of_stock_strains

        # Write strain data
        for strain in all_strains:
            row = [
                strain.get("id", ""),
                strain.get("name", ""),
                strain.get("breeder", ""),
                strain.get("indica", ""),
                strain.get("sativa", ""),
                "Yes" if strain.get("autoflower", False) else "No",
                strain.get("description", ""),
                strain.get("seed_count", ""),
                strain.get("cycle_time", ""),
                strain.get("url", ""),
                strain.get("short_description", ""),
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting strains to CSV: {e}")
        return None


def export_activities_csv():
    """
    Export all plant activities to CSV format.

    Returns:
        str: CSV data as string
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
        activities = PlantActivity.query.join(Plant).all()

        # Write activity data
        for activity in activities:
            row = [
                activity.id,
                activity.plant_id,
                activity.plant.name if activity.plant else "",
                activity.activity.name if activity.activity else activity.name,
                activity.name,
                activity.note or "",
                activity.date.strftime("%Y-%m-%d %H:%M:%S") if activity.date else "",
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting activities to CSV: {e}")
        return None


def export_users_csv():
    """
    Export all users to CSV format.

    Returns:
        str: CSV data as string
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
        users = get_all_users()

        # Write user data
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
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting users to CSV: {e}")
        return None


def export_plants_json():
    """
    Export all plants to JSON format.

    Returns:
        str: JSON data as string
    """
    try:
        # Get all plants with detailed information
        living_plants = get_living_plants()
        harvested_plants = get_harvested_plants()
        dead_plants = get_dead_plants()

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "export_type": "plants",
            "living_plants": living_plants,
            "harvested_plants": harvested_plants,
            "dead_plants": dead_plants,
            "total_plants": len(living_plants)
            + len(harvested_plants)
            + len(dead_plants),
        }

        return json.dumps(export_data, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error exporting plants to JSON: {e}")
        return None


def export_strains_json():
    """
    Export all strains to JSON format.

    Returns:
        str: JSON data as string
    """
    try:
        # Get all strains
        in_stock_strains = get_in_stock_strains()
        out_of_stock_strains = get_out_of_stock_strains()

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "export_type": "strains",
            "in_stock_strains": in_stock_strains,
            "out_of_stock_strains": out_of_stock_strains,
            "total_strains": len(in_stock_strains) + len(out_of_stock_strains),
        }

        return json.dumps(export_data, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error exporting strains to JSON: {e}")
        return None


def export_complete_backup():
    """
    Create a complete backup of all application data in ZIP format.

    Returns:
        BytesIO: ZIP file containing all data exports
    """
    try:
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Add timestamp to backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Export plants
            plants_csv = export_plants_csv()
            if plants_csv:
                zip_file.writestr(f"plants_{timestamp}.csv", plants_csv)

            plants_json = export_plants_json()
            if plants_json:
                zip_file.writestr(f"plants_{timestamp}.json", plants_json)

            # Export strains
            strains_csv = export_strains_csv()
            if strains_csv:
                zip_file.writestr(f"strains_{timestamp}.csv", strains_csv)

            strains_json = export_strains_json()
            if strains_json:
                zip_file.writestr(f"strains_{timestamp}.json", strains_json)

            # Export activities
            activities_csv = export_activities_csv()
            if activities_csv:
                zip_file.writestr(f"activities_{timestamp}.csv", activities_csv)

            # Export users (admin only)
            users_csv = export_users_csv()
            if users_csv:
                zip_file.writestr(f"users_{timestamp}.csv", users_csv)

            # Export sensor data
            sensors_csv = export_sensors_csv()
            if sensors_csv:
                zip_file.writestr(f"sensors_{timestamp}.csv", sensors_csv)

            # Add metadata file
            metadata = {
                "backup_timestamp": datetime.now().isoformat(),
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
        return None


def export_sensors_csv():
    """
    Export sensor data to CSV format.

    Returns:
        str: CSV data as string
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
        sensors = Sensor.query.all()

        for sensor in sensors:
            # Get latest reading
            latest_reading = (
                SensorData.query.filter_by(sensor_id=sensor.id)
                .order_by(SensorData.created_at.desc())
                .first()
            )

            row = [
                sensor.id,
                sensor.name,
                sensor.zone.name if sensor.zone else "",
                sensor.source or "",
                sensor.device or "",
                sensor.type or "",
                sensor.unit or "",
                latest_reading.value if latest_reading else "",
                (
                    latest_reading.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if latest_reading
                    else ""
                ),
            ]
            writer.writerow(row)

        return output.getvalue()
    except Exception as e:
        logger.error(f"Error exporting sensors to CSV: {e}")
        return None


def get_export_statistics():
    """
    Get statistics about exportable data.

    Returns:
        dict: Export statistics
    """
    try:
        stats = {
            "total_plants": Plant.query.count(),
            "living_plants": Plant.query.filter(Plant.status_id.notin_([4, 5])).count(),
            "harvested_plants": Plant.query.filter_by(status_id=4).count(),
            "dead_plants": Plant.query.filter_by(status_id=5).count(),
            "total_strains": Strain.query.count(),
            "in_stock_strains": Strain.query.filter(Strain.seed_count > 0).count(),
            "out_of_stock_strains": Strain.query.filter(Strain.seed_count == 0).count(),
            "total_activities": PlantActivity.query.count(),
            "total_users": User.query.count(),
            "total_sensors": Sensor.query.count(),
            "total_sensor_readings": SensorData.query.count(),
            "last_export_date": "Never",  # This could be stored in settings
        }

        return stats
    except Exception as e:
        logger.error(f"Error getting export statistics: {e}")
        return {
            "total_plants": 0,
            "living_plants": 0,
            "harvested_plants": 0,
            "dead_plants": 0,
            "total_strains": 0,
            "in_stock_strains": 0,
            "out_of_stock_strains": 0,
            "total_activities": 0,
            "total_users": 0,
            "total_sensors": 0,
            "total_sensor_readings": 0,
            "last_export_date": "Never",
        }
