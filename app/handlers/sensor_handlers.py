"""
Sensor handlers for the CultivAR application.
"""

from datetime import datetime, timedelta

import requests

from app.logger import logger
from app.models import db
from app.models.acinfinity_models import ACInfinityDevice, ACInfinityToken
from app.models.base_models import Sensor, SensorData, Zone
from app.models.ecowitt_models import EcowittDevice
from app.utils.helpers import parse_date


def get_sensors():
    """
    Get all sensors.

    Returns:
        list: The sensors.
    """
    try:
        sensors = Sensor.query.all()

        sensor_list = []
        for sensor in sensors:
            # Get the latest reading for this sensor
            latest_reading = (
                SensorData.query.filter_by(sensor_id=sensor.id)
                .order_by(SensorData.created_at.desc())
                .first()
            )

            sensor_data = {
                "id": sensor.id,
                "name": sensor.name,
                "zone": sensor.zone_name,
                "source": sensor.source,
                "device": sensor.device,
                "type": sensor.type,
                "show": sensor.show,
                "unit": sensor.unit,
                "create_dt": sensor.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "update_dt": sensor.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "latest_reading": (
                    {
                        "value": latest_reading.value,
                        "date": latest_reading.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    if latest_reading
                    else None
                ),
            }

            sensor_list.append(sensor_data)

        return sensor_list
    except Exception as e:
        logger.error(f"Error getting sensors: {e}")
        return []


def get_grouped_sensors_with_latest_reading():
    """
    Get sensors grouped by zone with their latest readings.

    Returns:
        dict: The grouped sensors.
    """
    try:
        # Get all zones
        zones = Zone.query.all()

        grouped_sensors = {}

        for zone in zones:
            # Get sensors for this zone
            sensors = Sensor.query.filter_by(zone_id=zone.id, show=True).all()

            sensor_list = []
            for sensor in sensors:
                # Get the latest reading for this sensor
                latest_reading = (
                    SensorData.query.filter_by(sensor_id=sensor.id)
                    .order_by(SensorData.created_at.desc())
                    .first()
                )

                if latest_reading:
                    sensor_data = {
                        "id": sensor.id,
                        "name": sensor.name,
                        "unit": sensor.unit,
                        "value": latest_reading.value,
                        "date": latest_reading.created_at,
                    }

                    sensor_list.append(sensor_data)

            if sensor_list:
                grouped_sensors[zone.name] = sensor_list

        return grouped_sensors
    except Exception as e:
        logger.error(f"Error getting grouped sensors: {e}")
        return {}


def get_sensor_data(sensor_id, start_date=None, end_date=None):
    """
    Get sensor data for a specific sensor.

    Args:
        sensor_id (int): The ID of the sensor.
        start_date (str, optional): The start date for the data.
        end_date (str, optional): The end date for the data.

    Returns:
        dict: The sensor data.
    """
    try:
        sensor = Sensor.query.get(sensor_id)

        if not sensor:
            return {"success": False, "error": "Sensor not found"}

        # Parse dates
        start_dt = (
            parse_date(start_date) if start_date else datetime.now() - timedelta(days=7)
        )
        end_dt = parse_date(end_date) if end_date else datetime.now()

        # Get sensor data
        query = SensorData.query.filter_by(sensor_id=sensor_id)

        if start_dt:
            query = query.filter(SensorData.created_at >= start_dt)

        if end_dt:
            query = query.filter(SensorData.created_at <= end_dt)

        data = query.order_by(SensorData.created_at).all()

        # Format data for charts
        chart_data = {
            "sensor": {"id": sensor.id, "name": sensor.name, "unit": sensor.unit},
            "data": [
                {
                    "date": reading.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "value": reading.value,
                }
                for reading in data
            ],
        }

        return chart_data
    except Exception as e:
        logger.error(f"Error getting sensor data: {e}")
        return {"success": False, "error": str(e)}


def scan_ac_infinity_sensors():
    """
    Scan for AC Infinity sensors.

    Returns:
        dict: The result of the operation.
    """
    try:
        # Check if we have a valid token
        token = ACInfinityToken.query.order_by(
            ACInfinityToken.created_at.desc()
        ).first()

        if not token or token.expires_at < datetime.now():
            return {"success": False, "error": "No valid AC Infinity token found"}

        # Make API request to get devices
        headers = {"Authorization": f"Bearer {token.access_token}"}

        response = requests.get(
            "https://api.acinfinity.com/v2/devices", headers=headers
        )

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API request failed: {response.status_code}",
            }

        devices = response.json().get("data", [])

        # Process devices
        for device_data in devices:
            device_id = device_data.get("id")

            # Check if device already exists
            device = ACInfinityDevice.query.filter_by(device_id=device_id).first()

            if not device:
                # Create new device
                device = ACInfinityDevice(
                    device_id=device_id,
                    name=device_data.get("name"),
                    type=device_data.get("type"),
                    status=device_data.get("status"),
                )

                db.session.add(device)
            else:
                # Update existing device
                device.name = device_data.get("name", device.name)
                device.type = device_data.get("type", device.type)
                device.status = device_data.get("status", device.status)

            # Process sensors
            sensors = device_data.get("sensors", [])

            for sensor_data in sensors:
                # Check if sensor already exists
                sensor = Sensor.query.filter_by(
                    source="acinfinity", device=device_id, type=sensor_data.get("type")
                ).first()

                if not sensor:
                    # Create new sensor
                    sensor = Sensor(
                        name=f"{device.name} {sensor_data.get('type').capitalize()}",
                        zone_id=None,
                        source="acinfinity",
                        device=device_id,
                        type=sensor_data.get("type"),
                        show=True,
                        unit=get_sensor_unit(sensor_data.get("type")),
                    )

                    db.session.add(sensor)

                # Add sensor reading
                reading = SensorData(
                    sensor_id=sensor.id if sensor.id else None,
                    value=sensor_data.get("value", 0),
                )

                db.session.add(reading)

        db.session.commit()

        return {"success": True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error scanning AC Infinity sensors: {e}")
        return {"success": False, "error": str(e)}


def scan_ecowitt_sensors():
    """
    Scan for Ecowitt sensors.

    Returns:
        dict: The result of the operation.
    """
    try:
        # Get Ecowitt server from settings
        from app.handlers.settings_handlers import get_setting

        server = get_setting("ec_server")

        if not server:
            return {"success": False, "error": "Ecowitt server not configured"}

        # Make API request to get data
        response = requests.get(f"http://{server}/data/report")

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API request failed: {response.status_code}",
            }

        data = response.json()

        # Process device
        device_id = data.get("mac", "unknown")

        # Check if device already exists
        device = EcowittDevice.query.filter_by(device_id=device_id).first()

        if not device:
            # Create new device
            device = EcowittDevice(
                device_id=device_id,
                name=data.get("stationtype", "Ecowitt Device"),
                ip_address=server,
                mac_address=device_id,
            )

            db.session.add(device)
        else:
            # Update existing device
            device.name = data.get("stationtype", device.name)
            device.ip_address = server

        # Process sensors
        sensor_types = [
            {"key": "soilmoisture1", "name": "Soil Moisture 1", "unit": "%"},
            {"key": "soilmoisture2", "name": "Soil Moisture 2", "unit": "%"},
            {"key": "soilmoisture3", "name": "Soil Moisture 3", "unit": "%"},
            {"key": "soilmoisture4", "name": "Soil Moisture 4", "unit": "%"},
            {"key": "soiltemp1f", "name": "Soil Temperature 1", "unit": "°F"},
            {"key": "soiltemp2f", "name": "Soil Temperature 2", "unit": "°F"},
            {"key": "soiltemp3f", "name": "Soil Temperature 3", "unit": "°F"},
            {"key": "soiltemp4f", "name": "Soil Temperature 4", "unit": "°F"},
        ]

        for sensor_type in sensor_types:
            key = sensor_type["key"]
            value = data.get(key)

            if value is not None:
                # Check if sensor already exists
                sensor = Sensor.query.filter_by(
                    source="ecowitt", device=device_id, type=key
                ).first()

                if not sensor:
                    # Create new sensor
                    sensor = Sensor(
                        name=sensor_type["name"],
                        zone_id=None,
                        source="ecowitt",
                        device=device_id,
                        type=key,
                        show=True,
                        unit=sensor_type["unit"],
                    )

                    db.session.add(sensor)
                    db.session.flush()  # Get the sensor ID

                # Add sensor reading
                reading = SensorData(sensor_id=sensor.id, value=float(value))

                db.session.add(reading)

        db.session.commit()

        return {"success": True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error scanning Ecowitt sensors: {e}")
        return {"success": False, "error": str(e)}


def edit_sensor(data):
    """
    Edit a sensor.

    Args:
        data (dict): The sensor data.

    Returns:
        dict: The result of the operation.
    """
    try:
        sensor_id = data.get("id")
        sensor = Sensor.query.get(sensor_id)

        if not sensor:
            return {"success": False, "error": "Sensor not found"}

        # Update sensor fields
        sensor.name = data.get("name", sensor.name)
        sensor.zone_id = data.get("zone_id", sensor.zone_id)
        sensor.show = data.get("show", sensor.show)

        db.session.commit()

        return {"success": True, "sensor_id": sensor.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error editing sensor: {e}")
        return {"success": False, "error": str(e)}


def delete_sensor(sensor_id):
    """
    Delete a sensor.

    Args:
        sensor_id (int): The ID of the sensor.

    Returns:
        dict: The result of the operation.
    """
    try:
        sensor = Sensor.query.get(sensor_id)

        if not sensor:
            return {"success": False, "error": "Sensor not found"}

        # Delete sensor data
        SensorData.query.filter_by(sensor_id=sensor_id).delete()

        # Delete the sensor
        db.session.delete(sensor)
        db.session.commit()

        return {"success": True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting sensor: {e}")
        return {"success": False, "error": str(e)}


def get_sensor_unit(sensor_type):
    """
    Get the unit for a sensor type.

    Args:
        sensor_type (str): The sensor type.

    Returns:
        str: The sensor unit.
    """
    units = {
        "temperature": "°F",
        "humidity": "%",
        "vpd": "kPa",
        "co2": "ppm",
        "light": "lux",
        "soil_moisture": "%",
        "soil_temperature": "°F",
    }

    return units.get(sensor_type, "")
