from datetime import datetime
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard", template_folder="../web/templates")


@dashboard_bp.route("/")
@login_required
def dashboard():
    """Render the main dashboard page."""
    return render_template("views/index.html", title="Dashboard")


@dashboard_bp.route("/plants")
@login_required
def plants():
    """Render the plants page."""
    # Import Plant model
    from app.models.base_models import Plant, Strain, Status, Zone

    # Get all plants for the current user
    plants_data = []
    try:
        plants_query = Plant.query.filter_by(user_id=current_user.id).all()
        for plant in plants_query:
            # Get related data
            strain = Strain.query.get(plant.strain_id) if plant.strain_id else None
            status = Status.query.get(plant.status_id) if plant.status_id else None
            zone = Zone.query.get(plant.zone_id) if plant.zone_id else None

            # Calculate age in days
            age = 0
            if plant.start_dt:
                age = (datetime.now() - plant.start_dt).days

            plants_data.append({
                'id': plant.id,
                'name': plant.name,
                'strain_name': strain.name if strain else 'Unknown',
                'status': status.name if status else 'Unknown',
                'zone': zone.name if zone else 'Unknown',
                'age': age,
                'image_url': plant.image_url
            })

        # Get filter options
        strains = [{'id': s.id, 'name': s.name} for s in Strain.query.all()]
        zones = [z.name for z in Zone.query.all()]
        statuses = [s.name for s in Status.query.all()]

    except Exception as e:
        current_app.logger.error(f"Error loading plants data: {e}")
        plants_data = []
        strains = []
        zones = []
        statuses = []

    return render_template("views/plants.html",
                          title="My Plants",
                          plants=plants_data,
                          strains=strains,
                          zones=zones,
                          statuses=statuses)


@dashboard_bp.route("/plant/<int:plant_id>")
@login_required
def plant(plant_id):
    """Render individual plant view."""
    from app.models.base_models import Plant, Strain, Status, Zone

    try:
        # Get the specific plant
        plant = Plant.query.filter_by(id=plant_id, user_id=current_user.id).first()
        if not plant:
            flash("Plant not found.", "danger")
            return redirect(url_for("dashboard.plants"))

        # Get related data
        strain = Strain.query.get(plant.strain_id) if plant.strain_id else None
        status = Status.query.get(plant.status_id) if plant.status_id else None
        zone = Zone.query.get(plant.zone_id) if plant.zone_id else None

        # Calculate age in days
        age = 0
        if plant.start_dt:
            age = (datetime.now() - plant.start_dt).days

        plant_data = {
            'id': plant.id,
            'name': plant.name,
            'strain_name': strain.name if strain else 'Unknown',
            'status': status.name if status else 'Unknown',
            'zone': zone.name if zone else 'Unknown',
            'age': age,
            'image_url': plant.image_url,
            'description': plant.description or '',
            'start_date': plant.start_dt.strftime('%Y-%m-%d') if plant.start_dt else '',
            'is_clone': plant.is_clone,
            'current_week': plant.current_week or 0,
            'current_day': plant.current_day or 0
        }

        return render_template("views/plant.html",
                              title=f"Plant: {plant.name}",
                              plant=plant_data)

    except Exception as e:
        current_app.logger.error(f"Error loading plant {plant_id}: {e}")
        flash("Error loading plant details.", "danger")
        return redirect(url_for("dashboard.plants"))
