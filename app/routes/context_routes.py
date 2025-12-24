"""
Context API routes for CultivAR.
Provides aggregated data for AI context injection.
"""

from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from sqlalchemy import func

from app.models import db
from app.models.base_models import Plant, PlantActivity, Sensor, SensorData, Zone
from app.utils.calculations import calculate_vpd

context_bp = Blueprint('context_bp', __name__, url_prefix='/api/context')

@context_bp.route('/plant/<int:plant_id>', methods=['GET'])
def get_plant_context(plant_id):
    """
    Get aggregated context for a specific plant.
    Includes identity, environmental data (current + 24h history), and recent logs.
    """
    try:
        # 1. Fetch Plant Identity
        plant = Plant.query.get(plant_id)
        if not plant:
            return jsonify({"error": "Plant not found"}), 404

        # Calculate age
        age_days = (datetime.utcnow() - plant.start_dt).days if plant.start_dt else 0

        plant_data = {
            "name": plant.name,
            "strain": plant.strain.name if plant.strain else "Unknown",
            "stage": plant.status.status if plant.status else "Unknown",
            "age_days": age_days,
            "zone_id": plant.zone_id
        }

        # 2. Fetch Recent Activity (Logs)
        # Limit to last 5 entries
        activities = (
            PlantActivity.query.filter_by(plant_id=plant_id)
            .order_by(PlantActivity.date.desc())
            .limit(5)
            .all()
        )
        
        recent_activity = []
        for activity in activities:
            date_str = activity.date.strftime("%Y-%m-%d")
            # Activity type name - handling relation
            activity_type = activity.activity.name if activity.activity else "Log"
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
            sensors = Sensor.query.filter_by(zone_id=plant.zone_id, show=True).all()
            
            # Current Readings
            current_readings = {}
            temp_f = None
            humidity = None
            
            for sensor in sensors:
                latest = SensorData.query.filter_by(sensor_id=sensor.id).order_by(SensorData.created_at.desc()).first()
                if latest:
                    # Simplify keys for AI context (lowercase, no spaces)
                    key = sensor.type.lower().replace(" ", "_")
                    current_readings[key] = latest.value
                    
                    if key == 'temperature':
                        temp_f = latest.value
                    elif key == 'humidity':
                        humidity = latest.value
            
            # Inject calculated VPD if possible
            if temp_f is not None and humidity is not None:
                current_readings['vpd'] = calculate_vpd(temp_f, humidity)
                
            environment_data["current"] = current_readings

            # 24h History Averages
            # We need to aggregate data for the last 24 hours for sensors in this zone
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            history_avgs = {}
            
            # We'll do a simplified aggregation by sensor type
            # This query joins SensorData -> Sensor to filter by Zone and Date
            results = db.session.query(
                Sensor.type,
                func.avg(SensorData.value).label('average_value'),
                func.min(SensorData.value).label('min_value'),
                func.max(SensorData.value).label('max_value')
            ).join(SensorData).filter(
                Sensor.zone_id == plant.zone_id,
                SensorData.created_at >= cutoff_time
            ).group_by(Sensor.type).all()

            for r in results:
                key = r.type.lower().replace(" ", "_")
                history_avgs[f"avg_{key}"] = round(r.average_value, 2)
                # optionally include min/max if useful, keeping it simple for now
            
            environment_data["history_24h"] = history_avgs

        # 4. Construct Final Response
        response = {
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "plant_id": plant_id
            },
            "plant": plant_data,
            "environment": environment_data,
            "recent_activity": recent_activity
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
