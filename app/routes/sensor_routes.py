"""
Sensor API routes for the CultivAR application.
Provides REST endpoints for sensor management and AC Infinity integration.
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.handlers.sensor_handlers import (
    get_sensors,
    get_sensor_data,
    scan_ac_infinity_sensors,
    edit_sensor,
    delete_sensor,
    get_grouped_sensors_with_latest_reading,
)
from app.logger import logger

sensor_bp = Blueprint('sensor', __name__, url_prefix='/api/sensors')


@sensor_bp.route('/', methods=['GET'])
@login_required
def get_sensors_route():
    """
    Get all sensors for the current user.

    Returns:
        JSON: List of sensor objects with latest readings
    """
    try:
        sensors = get_sensors()
        return jsonify({"success": True, "data": sensors})
    except Exception as e:
        logger.error(f"Error getting sensors: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@sensor_bp.route('/grouped', methods=['GET'])
@login_required
def get_grouped_sensors_route():
    """
    Get sensors grouped by zone with latest readings.

    Returns:
        JSON: Sensors grouped by zone
    """
    try:
        grouped_sensors = get_grouped_sensors_with_latest_reading()
        return jsonify({"success": True, "data": grouped_sensors})
    except Exception as e:
        logger.error(f"Error getting grouped sensors: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@sensor_bp.route('/<int:sensor_id>', methods=['GET'])
@login_required
def get_sensor_route(sensor_id):
    """
    Get detailed sensor data and readings for a specific sensor.

    Args:
        sensor_id (int): The sensor ID

    Returns:
        JSON: Sensor data with readings
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        data = get_sensor_data(sensor_id, start_date, end_date)

        if "success" in data and not data["success"]:
            return jsonify(data), 404

        return jsonify({"success": True, "data": data})
    except Exception as e:
        logger.error(f"Error getting sensor {sensor_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@sensor_bp.route('/scan/ac-infinity', methods=['POST'])
@login_required
def scan_ac_infinity_route():
    """
    Scan for AC Infinity devices and sensors.

    Returns:
        JSON: Scan results
    """
    try:
        result = scan_ac_infinity_sensors()
        status_code = 200 if result.get("success", False) else 400
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Error scanning AC Infinity sensors: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@sensor_bp.route('/', methods=['POST'])
@login_required
def create_sensor_route():
    """
    Create a new sensor.

    Body:
        JSON: Sensor creation data

    Returns:
        JSON: Created sensor data
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        # For now, return not implemented - would need additional handler
        logger.info(f"Create sensor request: {data}")
        return jsonify({
            "success": False,
            "error": "Sensor creation not yet implemented",
            "data": data
        }), 501
    except Exception as e:
        logger.error(f"Error creating sensor: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@sensor_bp.route('/<int:sensor_id>', methods=['PUT'])
@login_required
def update_sensor_route(sensor_id):
    """
    Update an existing sensor.

    Args:
        sensor_id (int): The sensor ID

    Body:
        JSON: Sensor update data

    Returns:
        JSON: Update result
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Add sensor_id to data for handler
        data["id"] = sensor_id

        result = edit_sensor(data)
        status_code = 200 if result.get("success", False) else 400
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Error updating sensor {sensor_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@sensor_bp.route('/<int:sensor_id>', methods=['DELETE'])
@login_required
def delete_sensor_route(sensor_id):
    """
    Delete a sensor.

    Args:
        sensor_id (int): The sensor ID

    Returns:
        JSON: Deletion result
    """
    try:
        result = delete_sensor(sensor_id)
        status_code = 200 if result.get("success", False) else 400
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Error deleting sensor {sensor_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@sensor_bp.route('/health', methods=['GET'])
@login_required
def sensor_health_route():
    """
    Get overall sensor system health status.

    Returns:
        JSON: Health status information
    """
    try:
        # Get basic sensor counts and status
        sensors = get_sensors()

        total_sensors = len(sensors)
        online_sensors = sum(1 for s in sensors if s.get("status") == "online")
        offline_sensors = total_sensors - online_sensors

        health_data = {
            "total_sensors": total_sensors,
            "online_sensors": online_sensors,
            "offline_sensors": offline_sensors,
            "health_percentage": (online_sensors / total_sensors * 100) if total_sensors > 0 else 0,
            "last_updated": sensors[0].get("update_dt") if sensors else None
        }

        return jsonify({"success": True, "data": health_data})
    except Exception as e:
        logger.error(f"Error getting sensor health: {e}")
        return jsonify({"success": False, "error": str(e)}), 500