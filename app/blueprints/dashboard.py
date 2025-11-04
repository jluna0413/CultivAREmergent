from datetime import datetime
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from app.logger import logger
from app.models_async import User, SystemActivity
from app.utils.async_flask_helpers import FlaskAsyncSessionManager

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard", template_folder="../web/templates")


@dashboard_bp.route("/")
@login_required
def dashboard():
    """Render the main dashboard page."""
    return render_template("views/index.html", title="Dashboard")


@dashboard_bp.route("/plants")
@login_required
async def plants():
    """Render the plants page."""
    from app.handlers.plant_handlers_async import get_living_plants
    from app.handlers.strain_handlers_async import get_all_strains
    
    plants_data = []
    strains = []
    zones = []
    statuses = []
    
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get plants, strains, and zones data using async handlers
            plants_data = await get_living_plants(session)
            strains = await get_all_strains(session)
            
            # TODO: Add zones and statuses async handlers when available
            zones = []  # Placeholder for zones
            statuses = []  # Placeholder for statuses
        
        return render_template("views/plants.html",
                              title="My Plants",
                              plants=plants_data,
                              strains=strains,
                              zones=zones,
                              statuses=statuses)
    except Exception as e:
        current_app.logger.error(f"Error loading plants data: {e}")
        flash("Error loading plants data.", "danger")
        return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.route("/plant/<int:plant_id>")
@login_required
async def plant(plant_id):
    """Render individual plant view."""
    from app.handlers.plant_handlers_async import get_plant
    
    try:
        async with FlaskAsyncSessionManager() as session:
            plant_data = await get_plant(plant_id, session)
            
            if not plant_data:
                flash("Plant not found.", "warning")
                return redirect(url_for("dashboard.plants"))
        
        return render_template("views/plant.html",
                              title=f"Plant: {plant_data['name']}",
                              plant=plant_data)

    except Exception as e:
        current_app.logger.error(f"Error loading plant {plant_id}: {e}")
        flash("Error loading plant details.", "danger")
        return redirect(url_for("dashboard.plants"))


@dashboard_bp.route("/sensors")
@login_required
async def sensors():
    """Render the sensors page."""
    from app.handlers.sensor_handlers_async import get_grouped_sensors_with_latest_reading

    try:
        async with FlaskAsyncSessionManager() as session:
            grouped_sensors = await get_grouped_sensors_with_latest_reading(session)
              
        total_sensors = grouped_sensors.get("total_sensors", 0)
        active_sensors = total_sensors  # All zones are considered active
        warning_sensors = 0  # Placeholder for actual warning logic

        return render_template("views/sensors.html",
                               title="My Sensors",
                               grouped_sensors=grouped_sensors,
                               total_sensors=total_sensors,
                               active_sensors=active_sensors,
                               warning_sensors=warning_sensors)
    except Exception as e:
        current_app.logger.error(f"Error loading sensors data: {e}")
        flash("Error loading sensors data.", "danger")
        return redirect(url_for("dashboard.dashboard"))
