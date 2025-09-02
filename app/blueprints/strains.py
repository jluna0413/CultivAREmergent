"""
Strain blueprint for the CultivAR application.
"""

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import login_required

from app.config.config import Config

strains_bp = Blueprint("strains", __name__, template_folder="../web/templates")


@strains_bp.route("/")
@login_required
def strains_page():
    """Render the strains collection page."""
    from app.models.base_models import Strain, Breeder

    try:
        # Get all strains
        strains_query = Strain.query.all()
        strains = []
        for strain in strains_query:
            # Get breeder name
            breeder = Breeder.query.get(strain.breeder_id) if strain.breeder_id else None

            strains.append({
                'id': strain.id,
                'name': strain.name,
                'breeder_id': strain.breeder_id,
                'breeder_name': breeder.name if breeder else 'Unknown',
                'indica': strain.indica,
                'sativa': strain.sativa,
                'autoflower': strain.autoflower,
                'cycle_time': strain.cycle_time,
                'seed_count': strain.seed_count,
                'url': strain.url,
                'description': strain.description,
                'short_description': strain.description[:100] + '...' if strain.description and len(strain.description) > 100 else strain.description or '',
                'type': 'indica' if strain.indica > strain.sativa else ('sativa' if strain.sativa > strain.indica else 'hybrid')
            })

        # Get breeders for filter dropdown
        breeders = [{'id': b.id, 'name': b.name} for b in Breeder.query.all()]

    except Exception as e:
        current_app.logger.error(f"Error loading strains data: {e}")
        strains = []
        breeders = []

    return render_template(
        "views/strains.html",
        title="Collection",
        strains=strains,
        breeders=breeders
    )


@strains_bp.route("/strains")
@login_required
def strains_page_collection():
    """Render the strains collection page (alternative route)."""
    return strains_page()


@strains_bp.route("/<int:strain_id>")
@login_required
def strain_detail(strain_id):
    """Render individual strain detail page."""
    from app.models.base_models import Strain, Breeder

    try:
        # Get the specific strain
        strain = Strain.query.get(strain_id)
        if not strain:
            flash("Strain not found.", "danger")
            return redirect("/")

        # Get breeder information
        breeder = Breeder.query.get(strain.breeder_id) if strain.breeder_id else None

        # Get all breeders for edit modal
        breeders = Breeder.query.all()

        # Prepare strain data
        strain_data = {
            'id': strain.id,
            'name': strain.name,
            'breeder_id': strain.breeder_id,
            'breeder_name': breeder.name if breeder else 'Unknown',
            'indica': strain.indica,
            'sativa': strain.sativa,
            'autoflower': strain.autoflower,
            'cycle_time': strain.cycle_time,
            'seed_count': strain.seed_count,
            'url': strain.url,
            'description': strain.description,
            'short_description': strain.description[:100] + '...' if strain.description and len(strain.description) > 100 else strain.description or ''
        }

        return render_template(
            "views/strain.html",
            title=f"Strain: {strain.name}",
            strain=strain_data,
            breeders=breeders
        )

    except Exception as e:
        current_app.logger.error(f"Error loading strain {strain_id}: {e}")
        flash("Error loading strain details.", "danger")
        return redirect("/")


@strains_bp.route("/add")
@login_required
def add_strain_page():
    """Render the add strain page."""
    return render_template(
        "views/add_strain.html", title="Add New Strain", breeders=Config.Breeders
    )


@strains_bp.route("/strains/add")
@login_required
def add_strain_page_legacy():
    """Render the add strain page (legacy route)."""
    return render_template(
        "views/add_strain.html", title="Add New Strain", breeders=Config.Breeders
    )
