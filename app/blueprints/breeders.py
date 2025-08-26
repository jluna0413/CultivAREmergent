"""
Breeder blueprint for the CultivAR application.
"""

from flask import Blueprint, render_template
from flask_login import login_required

breeders_bp = Blueprint("breeders", __name__, template_folder="../web/templates")


@breeders_bp.route("/breeders/add")
@login_required
def add_breeder():
    """Render the add breeder page."""
    return render_template("views/add_breeder.html", title="Add New Breeder")
