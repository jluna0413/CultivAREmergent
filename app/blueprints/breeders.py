"""
Breeder blueprint for the CultivAR application - ASYNC VERSION.
"""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.utils.async_flask_helpers import FlaskAsyncSessionManager
from app.handlers.breeder_handlers_async import (
    get_all_breeders, 
    get_breeder_by_id, 
    create_breeder, 
    update_breeder, 
    delete_breeder,
    search_breeders
)

breeders_bp = Blueprint("breeders", __name__, template_folder="../web/templates")


@breeders_bp.route("/")
@login_required
async def breeders_page():
    """Render the breeders collection page."""
    search_query = request.args.get('search', '')
    
    try:
        async with FlaskAsyncSessionManager() as session:
            if search_query:
                # Search breeders
                breeders = await search_breeders(search_query, session)
            else:
                # Get all breeders
                breeders = await get_all_breeders(session)
        
        return render_template(
            "views/breeders.html",
            title="Breeders Collection",
            breeders=breeders,
            search_query=search_query
        )

    except Exception as e:
        current_app.logger.error(f"Error loading breeders data: {e}")
        flash("Error loading breeders data.", "danger")
        return render_template(
            "views/breeders.html",
            title="Breeders Collection",
            breeders=[],
            search_query=search_query
        )


@breeders_bp.route("/breeders")
@login_required
async def breeders_page_legacy():
    """Render the breeders collection page (legacy route)."""
    return await breeders_page()


@breeders_bp.route("/add")
@login_required
async def add_breeder():
    """Render the add breeder page."""
    return render_template("views/add_breeder.html", title="Add New Breeder")


@breeders_bp.route("/breeders/add", methods=["POST"])
@login_required
async def create_breeder_route():
    """Handle breeder creation from form."""
    try:
        form_data = {
            "name": request.form.get("name"),
            "description": request.form.get("description", ""),
            "website": request.form.get("website", ""),
            "contact_info": request.form.get("contact_info", ""),
            "user_id": 1  # TODO: Get from current_user.id when available
        }
        
        async with FlaskAsyncSessionManager() as session:
            result = await create_breeder(form_data, session)
            
            if result["success"]:
                flash(result["message"], "success")
                return redirect(url_for("breeders.breeders_page"))
            else:
                flash(result["error"], "danger")
                return redirect(url_for("breeders.add_breeder"))
                
    except Exception as e:
        current_app.logger.error(f"Error creating breeder: {e}")
        flash("Error creating breeder.", "danger")
        return redirect(url_for("breeders.add_breeder"))


@breeders_bp.route("/<int:breeder_id>")
@login_required
async def breeder_detail(breeder_id):
    """Render individual breeder detail page."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get breeder data using async handler
            breeder_data = await get_breeder_by_id(breeder_id, session)
            
            if not breeder_data:
                flash("Breeder not found.", "warning")
                return redirect(url_for("breeders.breeders_page"))
        
        return render_template(
            "views/breeder.html",
            title=f"Breeder: {breeder_data['name']}",
            breeder=breeder_data
        )

    except Exception as e:
        current_app.logger.error(f"Error loading breeder {breeder_id}: {e}")
        flash("Error loading breeder details.", "danger")
        return redirect(url_for("breeders.breeders_page"))


@breeders_bp.route("/<int:breeder_id>/edit", methods=["GET", "POST"])
@login_required
async def edit_breeder(breeder_id):
    """Render edit breeder page and handle updates."""
    if request.method == "POST":
        return await update_breeder_route(breeder_id)
    
    # GET request - show edit form
    try:
        async with FlaskAsyncSessionManager() as session:
            breeder_data = await get_breeder_by_id(breeder_id, session)
            
            if not breeder_data:
                flash("Breeder not found.", "warning")
                return redirect(url_for("breeders.breeders_page"))
        
        return render_template(
            "views/edit_breeder.html",
            title=f"Edit: {breeder_data['name']}",
            breeder=breeder_data
        )

    except Exception as e:
        current_app.logger.error(f"Error loading breeder {breeder_id}: {e}")
        flash("Error loading breeder for editing.", "danger")
        return redirect(url_for("breeders.breeders_page"))


@breeders_bp.route("/<int:breeder_id>/update", methods=["POST"])
@login_required
async def update_breeder_route(breeder_id):
    """Handle breeder update from form."""
    try:
        form_data = {
            "name": request.form.get("name"),
            "description": request.form.get("description", ""),
            "website": request.form.get("website", ""),
            "contact_info": request.form.get("contact_info", ""),
            "user_id": 1  # TODO: Get from current_user.id when available
        }
        
        async with FlaskAsyncSessionManager() as session:
            result = await update_breeder(breeder_id, form_data, session)
            
            if result["success"]:
                flash(result["message"], "success")
                return redirect(url_for("breeders.breeder_detail", breeder_id=breeder_id))
            else:
                flash(result["error"], "danger")
                return redirect(url_for("breeders.edit_breeder", breeder_id=breeder_id))
                
    except Exception as e:
        current_app.logger.error(f"Error updating breeder {breeder_id}: {e}")
        flash("Error updating breeder.", "danger")
        return redirect(url_for("breeders.edit_breeder", breeder_id=breeder_id))


@breeders_bp.route("/<int:breeder_id>/delete", methods=["POST"])
@login_required
async def delete_breeder_route(breeder_id):
    """Handle breeder deletion."""
    try:
        async with FlaskAsyncSessionManager() as session:
            result = await delete_breeder(breeder_id, session)
            
            if result["success"]:
                flash(result["message"], "success")
            else:
                flash(result["error"], "danger")
                
    except Exception as e:
        current_app.logger.error(f"Error deleting breeder {breeder_id}: {e}")
        flash("Error deleting breeder.", "danger")
    
    return redirect(url_for("breeders.breeders_page"))
