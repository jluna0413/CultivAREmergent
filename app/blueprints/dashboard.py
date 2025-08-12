"""
Dashboard blueprint for the CultivAR application.
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.config.config import Config

dashboard_bp = Blueprint("dashboard", __name__, template_folder="../web/templates")


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    """Render the mobile-responsive dashboard."""
    return render_template("views/index.html", title="Dashboard")


@dashboard_bp.route("/market/seed-bank")
@login_required
def market_seed_bank():
    """Render the seed bank page."""
    return render_template("views/market/seed_bank.html", title="Seed Bank")


@dashboard_bp.route("/market/extensions")
@login_required
def market_extensions():
    """Render the extensions page."""
    return render_template("views/market/extensions.html", title="Extensions")


@dashboard_bp.route("/market/gear")
@login_required
def market_gear():
    """Render the gear page."""
    return render_template("views/market/gear.html", title="Grow Gear")


@dashboard_bp.route("/sensors")
@login_required
def sensors():
    """Render the sensors page."""
    return render_template("views/sensors.html", title="Sensors")


@dashboard_bp.route("/settings")
@login_required
def settings():
    """Render the settings page."""
    return render_template(
        "views/settings.html", title="Settings", settings=Config.DEFAULT_SETTINGS
    )


@dashboard_bp.route("/strains")
@login_required
def strains():
    """Render the strains page."""
    return render_template("views/strains.html", title="Strain Collection")


@dashboard_bp.route("/plants")
@login_required
def plants():
    """Render the plants page."""
    return render_template("views/plants.html", title="My Plants")
