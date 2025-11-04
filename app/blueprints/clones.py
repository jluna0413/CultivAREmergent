"""
Clone management blueprint for the CultivAR application - ASYNC VERSION.
"""

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.handlers.clone_handlers_async import (
    create_clone,
    delete_clone,
    get_clones,
    get_parent_plants,
    get_clone_statistics,
)
from app.utils.async_flask_helpers import FlaskAsyncSessionManager
from app.utils.validators import sanitize_text_field
from app.logger import logger

clones_bp = Blueprint(
    "clones", __name__, url_prefix="/clones", template_folder="../web/templates"
)


@clones_bp.route("/")
@login_required
async def dashboard():
    """Clone management dashboard."""
    try:
        async with FlaskAsyncSessionManager() as session:
            clone_stats = await get_clone_statistics(session)
            all_clones = await get_clones(session)
            
            return render_template(
                "clones/dashboard.html",
                title="Clone Management",
                clone_stats=clone_stats,
                clones=all_clones,
            )
    except Exception as e:
        logger.error(f"Error in clone dashboard: {e}")
        flash("Error loading clone data", "danger")
        return render_template(
            "clones/dashboard.html",
            title="Clone Management",
            clone_stats={"total": 0, "active": 0, "completed": 0},
            clones=[],
        )


@clones_bp.route("/create", methods=["GET", "POST"])
@login_required
async def create():
    """Create new clones from a parent plant."""
    if request.method == "POST":
        parent_id = request.form.get("parent_id")
        clone_count = int(request.form.get("clone_count", 1))

        if not parent_id:
            flash("Please select a parent plant.", "danger")
            return redirect(url_for("clones.create"))

        try:
            async with FlaskAsyncSessionManager() as session:
                # Build clone data list and create clones
                results = []
                for i in range(clone_count):
                    clone_name = request.form.get(f"clone_name_{i}", f"Clone {i+1}")
                    clone_description = request.form.get(f"clone_description_{i}", "")
                    zone_id = request.form.get(f"zone_id_{i}")
                    
                    # Sanitize HTML content to prevent XSS
                    sanitized_description, desc_error = sanitize_text_field(clone_description, "clone description")
                    start_date = request.form.get(f"start_date_{i}")

                    clone_data = {
                        "name": clone_name,
                        "description": sanitized_description,
                        "zone_id": int(zone_id) if zone_id else None,
                        "start_date": start_date,
                        "user_id": current_user.id,
                    }
                    
                    # Create individual clone
                    result = await create_clone(int(parent_id), clone_data, session)
                    results.append(result)

                # Check overall results
                successful_clones = [r for r in results if r.get("success")]
                failed_clones = [r for r in results if not r.get("success")]
                
                if successful_clones:
                    flash(f"Successfully created {len(successful_clones)} clone(s)!", "success")
                
                if failed_clones:
                    for failure in failed_clones:
                        flash(f"Error: {failure.get('error', 'Unknown error')}", "danger")
                        
                return redirect(url_for("clones.dashboard"))
            
        except Exception as e:
            logger.error(f"Error creating clones: {e}")
            flash(f"Error creating clones: {str(e)}", "danger")

    # GET request - show the form
    try:
        async with FlaskAsyncSessionManager() as session:
            parent_plants = await get_parent_plants(session)
            # Note: Zone query would need async implementation
            zones = []  # Placeholder - would need async Zone query
    except Exception as e:
        logger.error(f"Error loading parent plants: {e}")
        parent_plants = []
        zones = []

    return render_template(
        "clones/create.html",
        title="Create Clones",
        parent_plants=parent_plants,
        zones=zones,
    )


@clones_bp.route("/<int:clone_id>/lineage")
@login_required
async def lineage(clone_id):
    """View clone lineage (family tree)."""
    # For now, return placeholder lineage data
    # Full lineage implementation would be complex and require additional async logic
    lineage_data = {"success": True, "lineage": []}

    return render_template(
        "clones/lineage.html", title="Clone Lineage", lineage=lineage_data["lineage"]
    )


@clones_bp.route("/<int:clone_id>/delete", methods=["POST"])
@login_required
async def delete(clone_id):
    """Delete a clone."""
    try:
        async with FlaskAsyncSessionManager() as session:
            result = await delete_clone(clone_id, session)
            return jsonify(result)
    except Exception as e:
        logger.error(f"Error deleting clone {clone_id}: {e}")
        return jsonify({"success": False, "error": str(e)})


# API endpoints
@clones_bp.route("/api/stats")
@login_required
async def api_stats():
    """API endpoint to get clone statistics."""
    try:
        async with FlaskAsyncSessionManager() as session:
            stats = await get_clone_statistics(session)
            return jsonify({"success": True, "stats": stats})
    except Exception as e:
        logger.error(f"Error getting clone stats: {e}")
        return jsonify({"success": False, "error": str(e)})


@clones_bp.route("/api/parents")
@login_required
async def api_parents():
    """API endpoint to get available parent plants."""
    try:
        async with FlaskAsyncSessionManager() as session:
            parents = await get_parent_plants(session)
            return jsonify({"success": True, "parents": parents})
    except Exception as e:
        logger.error(f"Error getting parent plants: {e}")
        return jsonify({"success": False, "error": str(e)})


@clones_bp.route("/api")
@login_required
async def api_all():
    """API endpoint to get all clones."""
    try:
        async with FlaskAsyncSessionManager() as session:
            clones = await get_clones(session)
            return jsonify({"success": True, "clones": clones})
    except Exception as e:
        logger.error(f"Error getting clones: {e}")
        return jsonify({"success": False, "error": str(e)})


@clones_bp.route("/api/<int:clone_id>/lineage")
@login_required
async def api_lineage(clone_id):
    """API endpoint to get clone lineage."""
    # For now, return placeholder lineage data
    lineage_result = {"success": True, "lineage": []}
    return jsonify(lineage_result)
