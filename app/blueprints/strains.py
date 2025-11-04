"""
Strain blueprint for the CultivAR application - ASYNC VERSION.
"""

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import login_required

from app.config.config import Config
from app.utils.async_flask_helpers import FlaskAsyncSessionManager
from app.handlers.strain_handlers_async import get_all_strains, get_strain_by_id

strains_bp = Blueprint("strains", __name__, template_folder="../web/templates")


@strains_bp.route("/")
@login_required
async def strains_page():
    """Render the strains collection page."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get all strains using async handler
            strains = await get_all_strains(session)
            
            # Get breeders for filter dropdown
            breeders = [{'id': 1, 'name': 'Unknown Breeder'}]  # Placeholder
        
        return render_template(
            "views/strains.html",
            title="Collection",
            strains=strains,
            breeders=breeders
        )

    except Exception as e:
        current_app.logger.error(f"Error loading strains data: {e}")
        return render_template(
            "views/strains.html",
            title="Collection",
            strains=[],
            breeders=[]
        )


@strains_bp.route("/strains")
@login_required
async def strains_page_collection():
    """Render the strains collection page (alternative route)."""
    return await strains_page()


@strains_bp.route("/<int:strain_id>")
@login_required
async def strain_detail(strain_id):
    """Render individual strain detail page."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get strain data using async handler
            strain_data = await get_strain_by_id(strain_id, session)
            
            if not strain_data:
                # Fallback data if strain not found
                strain_data = {
                    'id': strain_id,
                    'name': f'Strain #{strain_id}',
                    'breeder_id': 1,
                    'breeder_name': 'Unknown Breeder',
                    'indica': 50,
                    'sativa': 50,
                    'autoflower': False,
                    'cycle_time': None,
                    'seed_count': 0,
                    'url': '',
                    'description': 'Strain details not found',
                    'short_description': 'Strain details not found'
                }

            # Get all breeders for edit modal
            breeders = [{'id': 1, 'name': 'Unknown Breeder'}]  # Placeholder

        return render_template(
            "views/strain.html",
            title=f"Strain: {strain_data['name']}",
            strain=strain_data,
            breeders=breeders
        )

    except Exception as e:
        current_app.logger.error(f"Error loading strain {strain_id}: {e}")
        flash("Error loading strain details.", "danger")
        return redirect("/")


@strains_bp.route("/add")
@login_required
async def add_strain_page():
    """Render the add strain page."""
    return render_template(
        "views/add_strain.html", title="Add New Strain", breeders=Config.Breeders
    )


@strains_bp.route("/strains/add")
@login_required
async def add_strain_page_legacy():
    """Render the add strain page (legacy route)."""
    return render_template(
        "views/add_strain.html", title="Add New Strain", breeders=Config.Breeders
    )
