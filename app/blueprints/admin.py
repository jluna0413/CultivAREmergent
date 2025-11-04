"""
Admin blueprint for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime, timedelta
from io import BytesIO

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required

from app.handlers.export_handlers_async import (
    export_activities_csv,
    export_complete_backup,
    export_plants_csv,
    export_plants_json,
    export_sensors_csv,
    export_strains_csv,
    export_strains_json,
    export_users_csv,
    get_export_statistics,
    delete_plant_async,
)
from app.handlers.user_handlers_async import (
    create_user_async,
    delete_user_async,
    force_password_reset_async,
    get_all_users_async,
    get_user_by_id_async,
    get_user_statistics_async,
    toggle_user_admin_status_async,
    update_user_async,
)
from app.utils.async_flask_helpers import FlaskAsyncSessionManager
from app.utils.rate_limiter import limiter
from app.logger import logger

admin_bp = Blueprint(
    "admin", __name__, url_prefix="/admin", template_folder="../web/templates"
)


@admin_bp.route("/")
@login_required
async def admin_redirect():
    """Redirect admin root page to /admin/users."""
    if not current_user.is_admin:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    return redirect(url_for("admin.users"))


@admin_bp.route("/users")
@login_required
async def users():
    """Admin page for user management."""
    if not current_user.is_admin:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    try:
        async with FlaskAsyncSessionManager() as session:
            # Get all users using async handler
            all_users = await get_all_users_async(session)
            # Get user statistics using async handler
            user_stats = await get_user_statistics_async(session)
    except Exception as e:
        logger.error(f"Error loading users data: {e}")
        flash("Error loading user data.", "danger")
        all_users = []
        user_stats = {"total": 0, "admin": 0, "regular": 0}

    return render_template(
        "admin/users.html",
        title="User Management",
        users=all_users,
        user_stats=user_stats,
    )


@limiter.limit("3 per minute")
@admin_bp.route("/users/create", methods=["GET", "POST"])
@login_required
async def create_user_route():
    """Create a new user."""
    if not current_user.is_admin:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        user_data = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "is_admin": request.form.get("is_admin") == "on",
            "force_password_change": request.form.get("force_password_change") == "on",
        }

        try:
            async with FlaskAsyncSessionManager() as session:
                result = await create_user_async(user_data, session)
                if result["success"]:
                    flash(f"User {user_data['username']} created successfully", "success")
                    return redirect(url_for("admin.users"))
                else:
                    flash(f"Error creating user: {result.get('error', 'Unknown error')}", "danger")
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            flash("Error creating user.", "danger")

    return render_template("admin/create_user.html", title="Create User")


@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
async def edit_user(user_id):
    """Edit an existing user."""
    if not current_user.is_admin:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    try:
        async with FlaskAsyncSessionManager() as session:
            # Get user data using async handler
            user_data = await get_user_by_id_async(user_id, session)
            
            if not user_data:
                flash("User not found.", "danger")
                return redirect(url_for("admin.users"))

            if request.method == "POST":
                update_data = {
                    "username": request.form.get("username", user_data["username"]),
                    "phone": request.form.get("phone", user_data["phone"]),
                    "email": request.form.get("email", user_data["email"]),
                    "is_admin": request.form.get("is_admin") == "on",
                    "force_password_change": request.form.get("force_password_change") == "on",
                }
                
                # Update password if provided
                new_password = request.form.get("password")
                if new_password:
                    update_data["password"] = new_password
                
                result = await update_user_async(user_id, update_data, session)
                if result["success"]:
                    flash(f"User {user_data['username']} updated successfully", "success")
                    return redirect(url_for("admin.users"))
                else:
                    flash(f"Error updating user: {result.get('error', 'Unknown error')}", "danger")

            return render_template("admin/edit_user.html", title="Edit User", user=user_data)
    except Exception as e:
        logger.error(f"Error editing user: {e}")
        flash("Error editing user.", "danger")
        return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
async def delete_user_route(user_id):
    """Delete a user."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        async with FlaskAsyncSessionManager() as session:
            result = await delete_user_async(user_id, session)
            return jsonify(result)
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return jsonify({"success": False, "error": "Error deleting user"})


@admin_bp.route('/users/bulk-delete', methods=['POST'])
@login_required
async def bulk_delete_users():
    """Bulk delete users by IDs (expects JSON {"user_ids": [1,2,3]})"""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"}), 403

    payload = request.get_json(silent=True) or {}
    user_ids = payload.get('user_ids') if isinstance(payload.get('user_ids'), list) else None
    if not user_ids:
        return jsonify({"success": False, "error": "No user_ids provided"}), 400

    try:
        # Convert to integers and filter out current admin to avoid self-delete
        ids = [int(uid) for uid in user_ids if int(uid) != current_user.id]
        if not ids:
            return jsonify({"success": False, "error": "No valid user IDs to delete"}), 400

        async with FlaskAsyncSessionManager() as session:
            # Delete users one by one
            results = []
            for user_id in ids:
                result = await delete_user_async(user_id, session)
                results.append(result)
            
            # Check if all deletions were successful
            successful = all(r["success"] for r in results)
            if successful:
                return jsonify({"success": True, "message": f"Successfully deleted {len(ids)} users"})
            else:
                failed_count = len([r for r in results if not r["success"]])
                return jsonify({"success": False, "error": f"Failed to delete {failed_count} users"})
    except Exception as e:
        logger.error(f"Bulk delete users failed: {e}")
        return jsonify({"success": False, "error": "Server error during bulk delete"}), 500


@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["POST"])
@login_required
async def toggle_user_admin(user_id):
    """Toggle admin status for a user."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        async with FlaskAsyncSessionManager() as session:
            result = await toggle_user_admin_status_async(user_id, session)
            return jsonify(result)
    except Exception as e:
        logger.error(f"Error toggling admin status: {e}")
        return jsonify({"success": False, "error": "Error toggling admin status"})


@admin_bp.route("/users/<int:user_id>/force-password-reset", methods=["POST"])
@login_required
async def force_password_reset_route(user_id):
    """Force password reset for a user."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        async with FlaskAsyncSessionManager() as session:
            result = await force_password_reset_async(user_id, session)
            return jsonify(result)
    except Exception as e:
        logger.error(f"Error forcing password reset: {e}")
        return jsonify({"success": False, "error": "Error forcing password reset"})


# API endpoints for AJAX requests
@admin_bp.route("/api/users")
@login_required
async def api_get_users():
    """API endpoint to get all users."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    # For now, return empty list placeholder
    users = []
    return jsonify({"success": True, "users": users})


@admin_bp.route("/api/users/<int:user_id>")
@login_required
async def api_get_user(user_id):
    """API endpoint to get a specific user."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    # For now, return placeholder user
    user = {"id": user_id, "username": "placeholder"}
    return jsonify({"success": True, "user": user})


@admin_bp.route("/api/users/stats")
@login_required
async def api_get_user_stats():
    """API endpoint to get user statistics."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    # For now, return placeholder stats
    stats = {"total": 0, "admin": 0, "regular": 0}
    return jsonify({"success": True, "stats": stats})


@admin_bp.route("/export")
@login_required
async def export():
    """Admin page for data export."""
    if not current_user.is_admin:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    # For now, return placeholder export stats
    export_stats = {"total_exports": 0, "last_export": None}

    return render_template(
        "admin/export.html", title="Data Export & Backup", export_stats=export_stats
    )


@admin_bp.route("/export/plants/<format>")
@login_required
async def export_plants_route(format):
    """Export plants data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        # For now, return placeholder data
        return jsonify({"success": False, "error": "Export functionality will be implemented with async handlers"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/export/strains/<format>")
@login_required
async def export_strains_route(format):
    """Export strains data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        # For now, return placeholder data
        return jsonify({"success": False, "error": "Export functionality will be implemented with async handlers"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/export/activities")
@login_required
async def export_activities_route():
    """Export activities data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        # For now, return placeholder data
        return jsonify({"success": False, "error": "Export functionality will be implemented with async handlers"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}) 


@admin_bp.route("/export/users")
@login_required
async def export_users_route():
    """Export users data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        async with FlaskAsyncSessionManager() as session:
            # Get export statistics using async handler
            export_stats = await get_export_statistics(session)
            return jsonify({"success": True, "stats": export_stats})
    except Exception as e:
        logger.error(f"Error in export_users_route: {e}")
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/export/sensors")
@login_required
async def export_sensors_route():
    """Export sensors data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        # For now, return placeholder data
        return jsonify({"success": False, "error": "Export functionality will be implemented with async handlers"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}) 


@admin_bp.route("/export/complete")
@login_required
async def export_complete_route():
    """Create complete system backup."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        # For now, return placeholder data
        return jsonify({"success": False, "error": "Backup functionality will be implemented with async handlers"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}) 


@admin_bp.route("/api/export/stats")
@login_required
async def api_export_stats_route():
    """API endpoint to get export statistics."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    # For now, return placeholder stats
    stats = {"total_exports": 0, "last_export": None}
    return jsonify({"success": True, "stats": stats})


# Helper function to check admin authentication
def admin_required(f):
    async def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({"error": "Admin login required"}), 401
        return await f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function


@admin_bp.route("/api/users", methods=["GET"])
@admin_required
async def get_users_api():
    """Get all users."""
    # For now, return placeholder user list
    user_list = []
    logger.info(f"User list: {user_list}")
    return jsonify(user_list)


@admin_bp.route("/api/users", methods=["POST"])
@admin_required
async def add_user_api():
    """Add a new user."""
    from app.logger import logger
    logger.info(f"add_user_api endpoint hit")
    logger.info(f"Request headers: {request.headers}")
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received in request.")
            return jsonify({"success": False, "error": "No JSON data received"}), 400
    except Exception as e:
        logger.error(f"Error getting JSON from request: {e}")
        return jsonify({"success": False, "error": "Could not parse JSON"}), 400

    logger.info(f"Received data for new user: {data}")
    # For now, return success placeholder
    result = {"success": True, "message": "User creation will be implemented with async handlers"}
    return jsonify(result), 201


@admin_bp.route("/api/users/<int:user_id>", methods=["GET"])
@admin_required
async def get_user_api(user_id):
    """Get a user by ID."""
    # For now, return placeholder user
    user_dict = {
        "id": user_id,
        "username": "placeholder",
        "email": "",
        "role": "user",
        "is_active": True,
        "last_login": None,
    }
    return jsonify(user_dict)


@admin_bp.route("/api/users/<int:user_id>", methods=["PUT"])
@admin_required
async def update_user_api(user_id):
    """Update a user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    # For now, return success placeholder
    return jsonify(
        {
            "id": user_id,
            "username": data.get("username", "placeholder"),
            "message": "User update will be implemented with async handlers",
        }
    )


@admin_bp.route("/api/users/<int:user_id>/reset-password", methods=["POST"])
@admin_required
async def reset_user_password_api(user_id):
    """Reset a user's password."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    if not data.get("new_password"):
        return jsonify({"error": "New password is required"}), 400

    # For now, return success placeholder
    return jsonify({"message": "Password reset will be implemented with async handlers"})


@admin_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
@admin_required
async def delete_user_api(user_id):
    """Delete a user."""
    # For now, return success placeholder
    return jsonify({"message": "User deletion will be implemented with async handlers"})


@admin_bp.route("/api/system/logs", methods=["GET"])
@admin_required
async def get_system_logs_api():
    """Get system logs."""
    # In a real application, this would read from a log file
    # For now, we'll return some sample logs
    logs = [
        {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "message": "Application started",
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
            "level": "INFO",
            "message": "User login: admin",
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(),
            "level": "ERROR",
            "message": "Database connection failed",
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=11)).isoformat(),
            "level": "INFO",
            "message": "Database connection restored",
        },
        {
            "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
            "level": "WARN",
            "message": "High temperature detected: 85.2°F",
        },
    ]

    return jsonify(logs)


@admin_bp.route("/api/system/info", methods=["GET"])
@admin_required
async def get_system_info_api():
    """Get system information."""
    import platform
    import sys

    # System info
    system_info = {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "os_name": platform.system(),
        "os_version": platform.version(),
    }

    # Try to get additional system info using psutil if available
    try:
        import psutil

        cpu_count = psutil.cpu_count()
        system_info["cpu_count"] = str(cpu_count) if cpu_count is not None else "N/A"
        system_info["memory_total"] = str(round(
            psutil.virtual_memory().total / (1024 * 1024 * 1024), 2
        ))  # GB
        system_info["memory_available"] = str(round(
            psutil.virtual_memory().available / (1024 * 1024 * 1024), 2
        ))  # GB
        system_info["disk_total"] = str(round(
            psutil.disk_usage("/").total / (1024 * 1024 * 1024), 2
        ))  # GB
        system_info["disk_free"] = str(round(
            psutil.disk_usage("/").free / (1024 * 1024 * 1024), 2
        ))  # GB
        system_info["boot_time"] = datetime.fromtimestamp(psutil.boot_time()).isoformat()
    except ImportError:
        # psutil not available, add some basic info
        system_info.update(
            {
                "cpu_count": "N/A",
                "memory_total": "N/A",
                "memory_available": "N/A",
                "disk_total": "N/A",
                "disk_free": "N/A",
                "boot_time": "N/A",
            }
        )

    return jsonify(system_info)


@admin_bp.route("/api/diagnostics/test", methods=["GET"])
async def diagnostics_test_api():
    """A simple endpoint for testing the diagnostics functionality."""
    import random
    import time

    # Simulate a delay
    time.sleep(0.5)

    # Return a test response
    return jsonify(
        {
            "success": True,
            "message": "Diagnostics test successful",
            "timestamp": time.time(),
            "random_value": random.random(),
            "test_array": [1, 2, 3, 4, 5],
            "test_object": {
                "name": "Test Object",
                "type": "Diagnostics",
                "enabled": True,
            },
        }
    )
