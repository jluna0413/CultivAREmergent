"""
Async sensor handlers for the CultivAR application.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from app.logger import logger
from app.models_async.grow import Zone
from app.models_async.sensors import Sensor, SensorData
from app.models_async.iot import ACInfinityDevice, ACInfinityToken, EcowittDevice
from app.utils.helpers import parse_date # Assuming this helper is async-compatible or pure

# --- Read Operations ---

async def get_sensors(session: AsyncSession):
    """
    Get all sensors with their latest readings.
    """
    try:
        stmt = select(Sensor).options(selectinload(Sensor.zone))
        result = await session.execute(stmt)
        sensors = result.scalars().all()

        sensor_list = []
        for sensor in sensors:
            latest_reading_result = await session.execute(
                select(SensorData)
                .where(SensorData.sensor_id == sensor.id)
                .order_by(desc(SensorData.timestamp))
                .limit(1)
            )
            latest_reading = latest_reading_result.scalar_one_or_none()

            sensor_data = {
                "id": sensor.id,
                "name": sensor.name,
                "zone": sensor.zone_name,
                "source": sensor.source,
                "device": sensor.device,
                "type": sensor.type,
                "show": sensor.show,
                "unit": sensor.unit,
                "created_at": sensor.created_at.strftime("%Y-%m-%d %H:%M:%S") if sensor.created_at else None,
                "updated_at": sensor.updated_at.strftime("%Y-%m-%d %H:%M:%S") if sensor.updated_at else None,
                "latest_reading": (
                    {
                        "value": latest_reading.value,
                        "date": latest_reading.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
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

async def get_grouped_sensors_with_latest_reading(session: AsyncSession):
    """
    Get sensors grouped by zone with their latest readings.
    """
    try:
        zones_result = await session.execute(select(Zone))
        zones = zones_result.scalars().all()

        grouped_sensors = {}
        for zone in zones:
            sensors_result = await session.execute(
                select(Sensor)
                .where(Sensor.zone_id == zone.id, Sensor.show == True)
                .options(selectinload(Sensor.data))
            )
            sensors = sensors_result.scalars().all()

            sensor_list = []
            for sensor in sensors:
                # Assuming data is ordered by timestamp descending in the relationship
                latest_reading = next(iter(sensor.data), None) # Get first item if exists

                if latest_reading:
                    sensor_data = {
                        "id": sensor.id,
                        "name": sensor.name,
                        "unit": sensor.unit,
                        "value": latest_reading.value,
                        "date": latest_reading.timestamp,
                    }
                    sensor_list.append(sensor_data)
            if sensor_list:
                grouped_sensors[zone.name] = sensor_list
        return grouped_sensors
    except Exception as e:
        logger.error(f"Error getting grouped sensors: {e}")
        return {}

async def get_sensor_data(session: AsyncSession, sensor_id: int, start_date: str = None, end_date: str = None):
    """
    Get sensor data for a specific sensor within a date range.
    """
    try:
        sensor = await session.get(Sensor, sensor_id)
        if not sensor:
            return {"success": False, "error": "Sensor not found"}

        start_dt = parse_date(start_date) if start_date else datetime.now(timezone.utc) - timedelta(days=7)
        end_dt = parse_date(end_date) if end_date else datetime.now(timezone.utc)

        stmt = (
            select(SensorData)
            .where(SensorData.sensor_id == sensor_id, SensorData.timestamp >= start_dt, SensorData.timestamp <= end_dt)
            .order_by(SensorData.timestamp)
        )
        result = await session.execute(stmt)
        data = result.scalars().all()

        chart_data = {
            "sensor": {"id": sensor.id, "name": sensor.name, "unit": sensor.unit},
            "data": [
                {
                    "date": reading.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "value": reading.value,
                }
                for reading in data
            ],
        }
        return chart_data
    except Exception as e:
        logger.error(f"Error getting sensor data: {e}")
        return {"success": False, "error": str(e)}

# --- Write Operations ---

async def scan_ac_infinity_sensors(session: AsyncSession):
    """
    Scan for AC Infinity sensors and update/create records.
    """
    try:
        token_result = await session.execute(select(ACInfinityToken).order_by(desc(ACInfinityToken.created_at)).limit(1))
        token = token_result.scalar_one_or_none()

        if not token or token.expires_at < datetime.now(timezone.utc):
            return {"success": False, "error": "No valid AC Infinity token found"}

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token.access_token}"}
            response = await client.get("https://api.acinfinity.com/v2/devices", headers=headers)
            response.raise_for_status()
            devices_data = response.json().get("data", [])

        for device_data in devices_data:
            device_id_str = device_data.get("id")
            device_stmt = select(ACInfinityDevice).where(ACInfinityDevice.device_id == device_id_str)
            device_obj = (await session.execute(device_stmt)).scalar_one_or_none()

            if not device_obj:
                device_obj = ACInfinityDevice(
                    device_id=device_id_str,
                    name=device_data.get("name"),
                    type=device_data.get("type"),
                    status=device_data.get("status"),
                )
                session.add(device_obj)
            else:
                device_obj.name = device_data.get("name", device_obj.name)
                device_obj.type = device_data.get("type", device_obj.type)
                device_obj.status = device_data.get("status", device_obj.status)
            await session.flush() # Ensure device_obj.id is available

            for sensor_data in device_data.get("sensors", []):
                sensor_type = sensor_data.get("type")
                sensor_stmt = select(Sensor).where(
                    Sensor.source == "acinfinity",
                    Sensor.ac_infinity_device_id == device_obj.id,
                    Sensor.type == sensor_type
                )
                sensor_obj = (await session.execute(sensor_stmt)).scalar_one_or_none()

                if not sensor_obj:
                    sensor_obj = Sensor(
                        name=f"{device_obj.name} {sensor_type.capitalize()}",
                        zone_id=None,
                        source="acinfinity",
                        ac_infinity_device_id=device_obj.id,
                        type=sensor_type,
                        show=True,
                        unit=get_sensor_unit(sensor_type),
                    )
                    session.add(sensor_obj)
                    await session.flush() # Ensure sensor_obj.id is available

                new_reading = SensorData(
                    sensor_id=sensor_obj.id,
                    value=sensor_data.get("value", 0),
                    sensor_type=sensor_type,
                    timestamp=datetime.now(timezone.utc)
                )
                session.add(new_reading)
        await session.commit()
        return {"success": True}
    except httpx.HTTPStatusError as e:
        await session.rollback()
        logger.error(f"AC Infinity API request failed: {e.response.status_code} - {e.response.text}")
        return {"success": False, "error": f"AC Infinity API error: {e.response.status_code}"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error scanning AC Infinity sensors: {e}")
        return {"success": False, "error": str(e)}

async def scan_ecowitt_sensors(session: AsyncSession):
    """
    Scan for Ecowitt sensors and update/create records.
    """
    try:
        # This would typically come from settings, but for now, hardcode or get from config
        # from app.handlers_async.settings_handlers import get_setting
        # server = await get_setting(session, "ec_server")
        server = "192.168.1.100" # Placeholder for Ecowitt server IP

        if not server:
            return {"success": False, "error": "Ecowitt server not configured"}

        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{server}/data/report")
            response.raise_for_status()
            data = response.json()

        device_id_str = data.get("mac", "unknown")
        device_stmt = select(EcowittDevice).where(EcowittDevice.device_id == device_id_str)
        device_obj = (await session.execute(device_stmt)).scalar_one_or_none()

        if not device_obj:
            device_obj = EcowittDevice(
                device_id=device_id_str,
                name=data.get("stationtype", "Ecowitt Device"),
                ip_address=server,
                mac_address=device_id_str,
            )
            session.add(device_obj)
        else:
            device_obj.name = data.get("stationtype", device_obj.name)
            device_obj.ip_address = server
        await session.flush() # Ensure device_obj.id is available

        sensor_types_map = {
            "soilmoisture1": {"name": "Soil Moisture 1", "unit": "%", "type": "soil_moisture"},
            "soilmoisture2": {"name": "Soil Moisture 2", "unit": "%", "type": "soil_moisture"},
            "soilmoisture3": {"name": "Soil Moisture 3", "unit": "%", "type": "soil_moisture"},
            "soilmoisture4": {"name": "Soil Moisture 4", "unit": "%", "type": "soil_moisture"},
            "soiltemp1f": {"name": "Soil Temperature 1", "unit": "°F", "type": "soil_temperature"},
            "soiltemp2f": {"name": "Soil Temperature 2", "unit": "°F", "type": "soil_temperature"},
            "soiltemp3f": {"name": "Soil Temperature 3", "unit": "°F", "type": "soil_temperature"},
            "soiltemp4f": {"name": "Soil Temperature 4", "unit": "°F", "type": "soil_temperature"},
        }

        for key, sensor_info in sensor_types_map.items():
            value = data.get(key)
            if value is not None:
                sensor_stmt = select(Sensor).where(
                    Sensor.source == "ecowitt",
                    Sensor.ecowitt_device_id == device_obj.id,
                    Sensor.type == sensor_info["type"] # Use generic type for sensor
                )
                sensor_obj = (await session.execute(sensor_stmt)).scalar_one_or_none()

                if not sensor_obj:
                    sensor_obj = Sensor(
                        name=sensor_info["name"],
                        zone_id=None,
                        source="ecowitt",
                        ecowitt_device_id=device_obj.id,
                        type=sensor_info["type"],
                        show=True,
                        unit=sensor_info["unit"],
                    )
                    session.add(sensor_obj)
                    await session.flush()

                new_reading = SensorData(
                    sensor_id=sensor_obj.id,
                    value=float(value),
                    sensor_type=sensor_info["type"],
                    timestamp=datetime.now(timezone.utc)
                )
                session.add(new_reading)
        await session.commit()
        return {"success": True}
    except httpx.HTTPStatusError as e:
        await session.rollback()
        logger.error(f"Ecowitt API request failed: {e.response.status_code} - {e.response.text}")
        return {"success": False, "error": f"Ecowitt API error: {e.response.status_code}"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error scanning Ecowitt sensors: {e}")
        return {"success": False, "error": str(e)}

async def edit_sensor(session: AsyncSession, sensor_id: int, data: Dict[str, Any]):
    """
    Edit a sensor's properties.
    """
    try:
        sensor = await session.get(Sensor, sensor_id)
        if not sensor:
            return {"success": False, "error": "Sensor not found"}

        sensor.name = data.get("name", sensor.name)
        sensor.zone_id = data.get("zone_id", sensor.zone_id)
        sensor.show = data.get("show", sensor.show)
        sensor.updated_at = datetime.now(timezone.utc)

        await session.commit()
        return {"success": True, "sensor_id": sensor.id}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error editing sensor: {e}")
        return {"success": False, "error": str(e)}

async def delete_sensor(session: AsyncSession, sensor_id: int):
    """
    Delete a sensor and its associated data.
    """
    try:
        sensor = await session.get(Sensor, sensor_id)
        if not sensor:
            return {"success": False, "error": "Sensor not found"}

        # SQLAlchemy cascade delete should handle SensorData if configured,
        # otherwise delete explicitly
        await session.execute(delete(SensorData).where(SensorData.sensor_id == sensor_id))
        await session.delete(sensor)
        await session.commit()
        return {"success": True}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting sensor: {e}")
        return {"success": False, "error": str(e)}

def get_sensor_unit(sensor_type: str) -> str:
    """
    Get the unit for a sensor type.
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
