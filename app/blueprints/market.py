"""
Market blueprint for the CultivAR application.
"""

from flask import Blueprint, render_template
from flask_login import login_required

market_bp = Blueprint("market", __name__)

@market_bp.route("/cart")
@login_required
def cart():
    """Render the shopping cart page."""
    return render_template("views/cart.html", title="Shopping Cart")

@market_bp.route("/market/seed-bank")
@login_required
def seed_bank():
    """Render the seed bank market page."""
    return render_template("views/market/seed_bank.html", title="Seed Bank")

@market_bp.route("/market/extensions")
@login_required
def extensions():
    """Render the extensions market page."""
    return render_template("views/market/extensions.html", title="Extensions")

@market_bp.route("/market/gear")
@login_required
def gear():
    """Render the gear market page."""
    return render_template("views/market/gear.html", title="Gear")