"""
Strain blueprint for the CultivAR application.
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.config.config import Config

strains_bp = Blueprint("strains", __name__, template_folder="../web/templates")


@strains_bp.route("/strains/add")
@login_required
def add_strain_page():
    """Render the add strain page."""
    return render_template(
        "views/add_strain.html", title="Add New Strain", breeders=Config.Breeders
    )
