"""
Sensor management handlers for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import SensorData, Zone, User, SystemActivity


async def get_all_sensors(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all sensors with their details - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of sensor data dictionaries.
    """
    try:
        # Simplified approach - since we may not have a dedicated Sensor model,
        # we'll create sensor data from Plant zones and other relevant data
        
        # Get zones and treat them as sensor locations
        result = await session.execute(select(Zone))
        zones = result.scalars().all()

        sensor_list = []
        for zone in zones:
            # Create sensor entry for each zone
            sensor_data = {
                "id": f"zone_{zone.id}",
                "name": f"Sensors - {zone.name}",
                "zone_id": zone.id,
                "zone_name": zone.name,
                "type": "environmental",
                "source": "system",
                "device": "cultivar_monitoring",
                "latest_reading": None,
                "latest_reading_date": None,
            }
            
            # Try to get latest reading for this zone
            latest_result = await session.execute(
                select(SensorData)
                .where(SensorData.zone_id == zone.id)
                .order_by(desc(SensorData.created_at))
                .limit(1)
            )
            latest_reading = latest_result.scalars().first()
            
            if latest_reading:
                sensor_data["latest_reading"] = latest_reading.value
                sensor_data["latest_reading_date"] = latest_reading.created_at.strftime("%Y-%m-%d %H:%M:%S")
            
            sensor_list.append(sensor_data)

        return sensor_list
    except Exception as e:
        logger.error(f"Error getting all sensors: {e}")
        return []


async def get_sensor_by_id(sensor_id: str, session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Get a specific sensor by ID - ASYNC VERSION.

    Args:
        sensor_id (str): The ID of the sensor.
        session: AsyncSession for database operations

    Returns:
        Optional[Dict[str, Any]]: Sensor data or None if not found.
    """
    try:
        if sensor_id.startswith("zone_"):
            zone_id = int(sensor_id.split("_")[1])
            result = await session.execute(select(Zone).where(Zone.id == zone_id))
            zone = result.scalars().first()
            
            if not zone:
                return None

            sensor_data = {
                "id": sensor_id,
                "name": f"Sensors - {zone.name}",
                "zone_id": zone.id,
                "zone_name": zone.name,
                "type": "environmental",
                "source": "system",
                "device": "cultivar_monitoring",
            }

            # Get latest reading
            latest_result = await session.execute(
                select(SensorData)
                .where(SensorData.zone_id == zone_id)
                .order_by(desc(SensorData.created_at))
                .limit(1)
            )
            latest_reading = latest_result.scalars().first()
            
            if latest_reading:
                sensor_data["latest_reading"] = latest_reading.value
                sensor_data["latest_reading_date"] = latest_reading.created_at.strftime("%Y-%m-%d %H:%M:%S")

            return sensor_data
        
        return None
    except Exception as e:
        logger.error(f"Error getting sensor by ID: {e}")
        return None


async def create_sensor_data(data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Create new sensor data - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): Sensor data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        # Create new sensor data
        new_sensor_data = SensorData(
            sensor_id=data.get("sensor_id"),
            zone_id=data.get("zone_id"),
            value=data.get("value"),
            unit=data.get("unit"),
            timestamp=data.get("timestamp") or datetime.now(),
        )

        session.add(new_sensor_data)
        await session.commit()
        await session.refresh(new_sensor_data)

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="sensor_data_created",
            details=f"Sensor data created: {new_sensor_data.value}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "sensor_data_id": new_sensor_data.id,
            "message": "Sensor data created successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating sensor data: {e}")
        return {"success": False, "error": str(e)}


async def get_sensor_readings(sensor_id: str, limit: int = 100, session: AsyncSession = None) -> List[Dict[str, Any]]:
    """
    Get sensor readings for a specific sensor - ASYNC VERSION.

    Args:
        sensor_id (str): The ID of the sensor.
        limit (int): Maximum number of readings to return.
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of sensor reading data dictionaries.
    """
    try:
        if sensor_id.startswith("zone_"):
            zone_id = int(sensor_id.split("_")[1])
            result = await session.execute(
                select(SensorData)
                .where(SensorData.zone_id == zone_id)
                .order_by(desc(SensorData.created_at))
                .limit(limit)
            )
            readings = result.scalars().all()

            reading_list = []
            for reading in readings:
                reading_data = {
                    "id": reading.id,
                    "sensor_id": sensor_id,
                    "zone_id": zone_id,
                    "value": reading.value,
                    "unit": reading.unit or "",
                    "timestamp": reading.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                reading_list.append(reading_data)

            return reading_list
        
        return []
    except Exception as e:
        logger.error(f"Error getting sensor readings: {e}")
        return []


async def get_sensor_statistics(session: AsyncSession) -> Dict[str, Any]:
    """
    Get sensor-related statistics - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Sensor statistics.
    """
    try:
        # Get total zones (acting as sensor locations)
        zones_result = await session.execute(select(Zone))
        zones = zones_result.scalars().all()
        
        # Get total sensor readings
        readings_result = await session.execute(select(SensorData))
        readings = readings_result.scalars().all()

        # Get readings from last 24 hours
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        recent_readings_result = await session.execute(
            select(SensorData).where(SensorData.created_at >= twenty_four_hours_ago)
        )
        recent_readings = recent_readings_result.scalars().all()

        stats = {
            "total_sensors": len(zones),
            "total_readings": len(readings),
            "recent_readings": len(recent_readings),
            "active_zones": len(zones),
        }

        return stats
    except Exception as e:
        logger.error(f"Error getting sensor statistics: {e}")
        return {
            "total_sensors": 0,
            "total_readings": 0,
            "recent_readings": 0,
            "active_zones": 0,
        }


async def get_grouped_sensors_with_latest_reading(session: AsyncSession) -> Dict[str, Any]:
    """
    Get sensors grouped by type, zone, and source with latest readings - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Grouped sensor data.
    """
    try:
        # Get all zones as sensor locations
        zones_result = await session.execute(select(Zone))
        zones = result.scalars().all()

        sensors_by_type = {}
        sensors_by_zone = {}
        sensors_by_source = {}

        for zone in zones:
            # Group by type
            sensor_type = "environmental"
            if sensor_type not in sensors_by_type:
                sensors_by_type[sensor_type] = 0
            sensors_by_type[sensor_type] += 1

            # Group by zone
            zone_name = zone.name
            if zone_name not in sensors_by_zone:
                sensors_by_zone[zone_name] = 0
            sensors_by_zone[zone_name] += 1

            # Group by source
            source = "system"
            if source not in sensors_by_source:
                sensors_by_source[source] = 0
            sensors_by_source[source] += 1

        return {
            "sensors_by_type": sensors_by_type,
            "sensors_by_zone": sensors_by_zone,
            "sensors_by_source": sensors_by_source,
            "total_sensors": len(zones),
        }
    except Exception as e:
        logger.error(f"Error getting grouped sensors: {e}")
        return {
            "sensors_by_type": {},
            "sensors_by_zone": {},
            "sensors_by_source": {},
            "total_sensors": 0,
        }


async def delete_sensor_data(sensor_data_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Delete sensor data - ASYNC VERSION.

    Args:
        sensor_data_id (int): The ID of the sensor data to delete.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(SensorData).where(SensorData.id == sensor_data_id))
        sensor_data = result.scalars().first()
        
        if not sensor_data:
            return {"success": False, "error": "Sensor data not found"}

        await session.delete(sensor_data)
        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=1,  # System user
            type="sensor_data_deleted",
            details=f"Sensor data deleted: ID {sensor_data_id}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {"success": True, "message": "Sensor data deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting sensor data: {e}")
        return {"success": False, "error": str(e)}