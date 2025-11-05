"""
Cultivar blueprint for the CultivAR application - ASYNC VERSION.
"""

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import login_required

from app.config.config import Config
from app.utils.async_flask_helpers import FlaskAsyncSessionManager
from app.handlers.cultivar_handlers_async import get_all_cultivars, get_cultivar_by_id

cultivars_bp = Blueprint("cultivars", __name__, template_folder="../web/templates")


@cultivars_bp.route("/")
@login_required
async def cultivars_page():
    """Render the cultivars collection page."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get all cultivars using async handler
            cultivars = await get_all_cultivars(session)
            
            # Get breeders for filter dropdown
            breeders = [{'id': 1, 'name': 'Unknown Breeder'}]  # Placeholder
        
        return render_template(
            "views/cultivars.html",
            title="Collection",
            cultivars=cultivars,
            breeders=breeders
        )

    except Exception as e:
        current_app.logger.error(f"Error loading cultivars data: {e}")
        return render_template(
            "views/cultivars.html",
            title="Collection",
            cultivars=[],
            breeders=[]
        )


@cultivars_bp.route("/cultivars")
@login_required
async def cultivars_page_collection():
    """Render the cultivars collection page (alternative route)."""
    return await cultivars_page()


@cultivars_bp.route("/<int:cultivar_id>")
@login_required
async def cultivar_detail(cultivar_id):
    """Render individual cultivar detail page."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get cultivar data using async handler
            cultivar_data = await get_cultivar_by_id(cultivar_id, session)
            
            if not cultivar_data:
                # Fallback data if cultivar not found
                cultivar_data = {
                    'id': cultivar_id,
                    'name': f'Cultivar #{cultivar_id}',
                    'breeder_id': 1,
                    'breeder_name': 'Unknown Breeder',
                    'indica': 50,
                    'sativa': 50,
                    'autoflower': False,
                    'cycle_time': None,
                    'seed_count': 0,
                    'url': '',
                    'description': 'Cultivar details not found',
                    'short_description': 'Cultivar details not found'
                }

            # Get all breeders for edit modal
            breeders = [{'id': 1, 'name': 'Unknown Breeder'}]  # Placeholder

        return render_template(
            "views/cultivar.html",
            title=f"Cultivar: {cultivar_data['name']}",
            cultivar=cultivar_data,
            breeders=breeders
        )

    except Exception as e:
        current_app.logger.error(f"Error loading cultivar {cultivar_id}: {e}")
        flash("Error loading cultivar details.", "danger")
        return redirect("/")


@cultivars_bp.route("/add")
@login_required
async def add_cultivar_page():
    """Render the add cultivar page."""
    return render_template(
        "views/add_cultivar.html", title="Add New Cultivar", breeders=Config.Breeders
    )


@cultivars_bp.route("/cultivars/add")
@login_required
async def add_cultivar_page_legacy():
    """Render the add cultivar page (legacy route)."""
    return render_template(
        "views/add_cultivar.html", title="Add New Cultivar", breeders=Config.Breeders
    )


# Backward compatibility aliases
strains_bp = cultivars_bp  # Alias for backward compatibility


@strains_bp.route("/")
@login_required
async def strains_page():
    """Legacy alias for cultivars_page"""
    return await cultivars_page()


@strains_bp.route("/strains")
@login_required
async def strains_page_collection():
    """Legacy alias for cultivars_page_collection"""
    return await cultivars_page()


@strains_bp.route("/<int:strain_id>")
@login_required
async def strain_detail(strain_id):
    """Legacy alias for cultivar_detail"""
    return await cultivar_detail(strain_id)


@strains_bp.route("/add")
@login_required
async def add_strain_page():
    """Legacy alias for add_cultivar_page"""
    return await add_cultivar_page()


@strains_bp.route("/strains/add")
@login_required
async def add_strain_page_legacy():
    """Legacy alias for add_cultivar_page_legacy"""
    return await add_cultivar_page_legacy()