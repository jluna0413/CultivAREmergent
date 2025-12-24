"""
Context Service
Aggregates plant, environmental, and activity data for AI context.
"""
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.models_async.grow import Plant, Zone
from app.models_async.activities import PlantActivity, ActivityType
from app.models_async.sensors import Sensor, SensorData
from app.utils.calculations import calculate_vpd

class ContextService:
    @staticmethod
    async def get_plant_context(plant_id: int, user_id: int, db: AsyncSession):
        """
        Get aggregated context for a specific plant.
        Includes identity, environmental data (current + 24h history), and recent logs.
        Returns a dictionary or raises exceptions.
        """
        
        # 1. Fetch Plant Identity with relationships
        query = select(Plant).options(
            selectinload(Plant.status),
            selectinload(Plant.cultivar),
            selectinload(Plant.zone)
        ).where(Plant.id == plant_id)
        
        result = await db.execute(query)
        plant = result.scalar_one_or_none()

        if not plant:
            return None # Handle 404 in caller
        
        # Verify ownership
        if plant.user_id != user_id:
            raise PermissionError("Not authorized")

        # Calculate age
        age_days = (datetime.utcnow() - plant.start_dt).days if plant.start_dt else 0

        plant_data = {
            "name": plant.name,
            "strain": plant.strain_name or "Unknown",
            "stage": plant.status_name or "Unknown",
            "age_days": age_days,
            "zone_id": plant.zone_id
        }

        # 2. Fetch Recent Activity (Logs)
        activity_query = select(PlantActivity).options(
            selectinload(PlantActivity.activity_type_rel)
        ).where(
            PlantActivity.plant_id == plant_id
        ).order_by(
            desc(PlantActivity.date)
        ).limit(5)
        
        ac_result = await db.execute(activity_query)
        activities = ac_result.scalars().all()
        
        recent_activity = []
        for activity in activities:
            date_str = activity.date.strftime("%Y-%m-%d")
            activity_type = activity.activity_type_rel.name if activity.activity_type_rel else "Log"
            note = f": {activity.note}" if activity.note else ""
            recent_activity.append(f"{date_str}: [{activity_type}] {note}")


        # 3. Fetch Environment Data
        environment_data = {
            "zone": "Unknown",
            "current": {},
            "history_24h": {}
        }

        if plant.zone:
            environment_data["zone"] = plant.zone.name
            
            # Get all sensors in the zone
            sensor_query = select(Sensor).where(Sensor.zone_id == plant.zone_id, Sensor.show == True)
            s_result = await db.execute(sensor_query)
            sensors = s_result.scalars().all()
            
            # Current Readings
            current_readings = {}
            temp_f = None
            humidity = None
            
            for sensor in sensors:
                data_query = select(SensorData).where(
                    SensorData.sensor_id == sensor.id
                ).order_by(
                    desc(SensorData.created_at)
                ).limit(1)
                
                d_result = await db.execute(data_query)
                latest = d_result.scalar_one_or_none()
                
                if latest:
                    key = (sensor.sensor_type or "unknown").lower().replace(" ", "_")
                    current_readings[key] = latest.value
                    
                    if key == 'temperature':
                        temp_f = latest.value
                    elif key == 'humidity':
                        humidity = latest.value
            
            # Inject calculated VPD
            if temp_f is not None and humidity is not None:
                current_readings['vpd'] = calculate_vpd(temp_f, humidity)
                
            environment_data["current"] = current_readings

            # 24h History Averages
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            history_avgs = {}
            
            hist_query = select(
                Sensor.sensor_type,
                func.avg(SensorData.value).label('average_value')
            ).join(
                Sensor, SensorData.sensor_id == Sensor.id
            ).where(
                Sensor.zone_id == plant.zone_id,
                SensorData.created_at >= cutoff_time
            ).group_by(
                Sensor.sensor_type
            )
            
            h_result = await db.execute(hist_query)
            history_data = h_result.all()

            for r in history_data:
                key = (r.sensor_type or "unknown").lower().replace(" ", "_")
                if r.average_value is not None:
                    history_avgs[f"avg_{key}"] = round(r.average_value, 2)
            
            environment_data["history_24h"] = history_avgs

        # 4. Construct Final Response
        return {
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "plant_id": plant_id
            },
            "plant": plant_data,
            "environment": environment_data,
            "recent_activity": recent_activity
        }
