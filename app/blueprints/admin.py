"""
Admin blueprint for the CultivAR application.
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

from app.handlers.export_handlers import (
    export_activities_csv,
    export_complete_backup,
    export_plants_csv,
    export_plants_json,
    export_sensors_csv,
    export_strains_csv,
    export_strains_json,
    export_users_csv,
    get_export_statistics,
)
from app.handlers.user_handlers import (
    create_user,
    delete_user,
    force_password_reset,
    get_all_users,
    get_user_by_id,
    get_user_statistics,
    toggle_user_admin_status,
    update_user,
)
from app.models import db
from app.models.base_models import User

admin_bp = Blueprint(
    "admin", __name__, url_prefix="/admin", template_folder="../web/templates"
)


@admin_bp.route("/users")
@login_required
def users():
    """Admin page for user management."""
    if not current_user.is_admin:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    all_users = get_all_users()
    user_stats = get_user_statistics()

    return render_template(
        "admin/users.html",
        title="User Management",
        users=all_users,
        user_stats=user_stats,
    )


@admin_bp.route("/users/create", methods=["GET", "POST"])
@login_required
def create_user_route():
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

        result = create_user(user_data)

        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("admin.users"))
        else:
            flash(result["error"], "danger")

    return render_template("admin/create_user.html", title="Create User")


@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    """Edit an existing user."""
    if not current_user.is_admin:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    user = get_user_by_id(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin.users"))

    if request.method == "POST":
        user_data = {
            "username": request.form.get("username"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "is_admin": request.form.get("is_admin") == "on",
            "force_password_change": request.form.get("force_password_change") == "on",
        }

        # Only update password if provided
        password = request.form.get("password")
        if password:
            user_data["password"] = password

        result = update_user(user_id, user_data)

        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("admin.users"))
        else:
            flash(result["error"], "danger")

    return render_template("admin/edit_user.html", title="Edit User", user=user)


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user_route(user_id):
    """Delete a user."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    result = delete_user(user_id)
    return jsonify(result)


@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["POST"])
@login_required
def toggle_user_admin(user_id):
    """Toggle admin status for a user."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    result = toggle_user_admin_status(user_id)
    return jsonify(result)


@admin_bp.route("/users/<int:user_id>/force-password-reset", methods=["POST"])
@login_required
def force_password_reset_route(user_id):
    """Force password reset for a user."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    result = force_password_reset(user_id)
    return jsonify(result)


# API endpoints for AJAX requests
@admin_bp.route("/api/users")
@login_required
def api_get_users():
    """API endpoint to get all users."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    users = get_all_users()
    return jsonify({"success": True, "users": users})


@admin_bp.route("/api/users/<int:user_id>")
@login_required
def api_get_user(user_id):
    """API endpoint to get a specific user."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    user = get_user_by_id(user_id)
    if user:
        return jsonify({"success": True, "user": user})
    else:
        return jsonify({"success": False, "error": "User not found"})


@admin_bp.route("/api/users/stats")
@login_required
def api_get_user_stats():
    """API endpoint to get user statistics."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    stats = get_user_statistics()
    return jsonify({"success": True, "stats": stats})


@admin_bp.route("/export")
@login_required
def export():
    """Admin page for data export."""
    if not current_user.is_admin:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    export_stats = get_export_statistics()

    return render_template(
        "admin/export.html", title="Data Export & Backup", export_stats=export_stats
    )


@admin_bp.route("/export/plants/<format>")
@login_required
def export_plants_route(format):
    """Export plants data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format.lower() == "csv":
            data = export_plants_csv()
            if data:
                return send_file(
                    BytesIO(data.encode("utf-8")),
                    mimetype="text/csv",
                    as_attachment=True,
                    download_name=f"cultivar_plants_{timestamp}.csv",
                )

        elif format.lower() == "json":
            data = export_plants_json()
            if data:
                return send_file(
                    BytesIO(data.encode("utf-8")),
                    mimetype="application/json",
                    as_attachment=True,
                    download_name=f"cultivar_plants_{timestamp}.json",
                )

        return jsonify({"success": False, "error": "Invalid format or export failed"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/export/strains/<format>")
@login_required
def export_strains_route(format):
    """Export strains data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format.lower() == "csv":
            data = export_strains_csv()
            if data:
                return send_file(
                    BytesIO(data.encode("utf-8")),
                    mimetype="text/csv",
                    as_attachment=True,
                    download_name=f"cultivar_strains_{timestamp}.csv",
                )

        elif format.lower() == "json":
            data = export_strains_json()
            if data:
                return send_file(
                    BytesIO(data.encode("utf-8")),
                    mimetype="application/json",
                    as_attachment=True,
                    download_name=f"cultivar_strains_{timestamp}.json",
                )

        return jsonify({"success": False, "error": "Invalid format or export failed"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/export/activities")
@login_required
def export_activities_route():
    """Export activities data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = export_activities_csv()

        if data:
            return send_file(
                BytesIO(data.encode("utf-8")),
                mimetype="text/csv",
                as_attachment=True,
                download_name=f"cultivar_activities_{timestamp}.csv",
            )

        return jsonify({"success": False, "error": "Export failed"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/export/users")
@login_required
def export_users_route():
    """Export users data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = export_users_csv()

        if data:
            return send_file(
                BytesIO(data.encode("utf-8")),
                mimetype="text/csv",
                as_attachment=True,
                download_name=f"cultivar_users_{timestamp}.csv",
            )

        return jsonify({"success": False, "error": "Export failed"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/export/sensors")
@login_required
def export_sensors_route():
    """Export sensors data."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = export_sensors_csv()

        if data:
            return send_file(
                BytesIO(data.encode("utf-8")),
                mimetype="text/csv",
                as_attachment=True,
                download_name=f"cultivar_sensors_{timestamp}.csv",
            )

        return jsonify({"success": False, "error": "Export failed"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/export/complete")
@login_required
def export_complete_route():
    """Create complete system backup."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_data = export_complete_backup()

        if backup_data:
            return send_file(
                backup_data,
                mimetype="application/zip",
                as_attachment=True,
                download_name=f"cultivar_complete_backup_{timestamp}.zip",
            )

        return jsonify({"success": False, "error": "Backup creation failed"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route("/api/export/stats")
@login_required
def api_export_stats_route():
    """API endpoint to get export statistics."""
    if not current_user.is_admin:
        return jsonify({"success": False, "error": "Access denied"})

    stats = get_export_statistics()
    return jsonify({"success": True, "stats": stats})


# Helper function to check admin authentication
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({"error": "Admin login required"}), 401
        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function


@admin_bp.route("/api/users", methods=["GET"])
@admin_required
def get_users_api():
    """Get all users."""
    users = User.query.all()

    # Convert users to a list of dictionaries
    user_list = []
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email if hasattr(user, "email") else "",
            "role": user.role if hasattr(user, "role") else "user",
            "is_active": True,  # In a real app, you'd check a status field
            "last_login": (
                user.last_login.isoformat()
                if hasattr(user, "last_login") and user.last_login
                else None
            ),
        }
        user_list.append(user_dict)

    return jsonify(user_list)


@admin_bp.route("/api/users", methods=["POST"])
@admin_required
def add_user_api():
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
    result = create_user(data)
    if result["success"]:
        return jsonify(result), 201
    else:
        logger.error(f"Error creating user: {result.get('error')}")
        return jsonify(result), 400


@admin_bp.route("/api/users/<int:user_id>", methods=["GET"])
@admin_required
def get_user_api(user_id):
    """Get a user by ID."""
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_dict = {
        "id": user.id,
        "username": user.username,
        "email": user.email if hasattr(user, "email") else "",
        "role": user.role if hasattr(user, "role") else "user",
        "is_active": True,  # In a real app, you'd check a status field
        "last_login": (
            user.last_login.isoformat()
            if hasattr(user, "last_login") and user.last_login
            else None
        ),
    }

    return jsonify(user_dict)


@admin_bp.route("/api/users/<int:user_id>", methods=["PUT"])
@admin_required
def update_user_api(user_id):
    """Update a user."""
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    # Update fields
    if data.get("username"):
        # Check if username already exists for another user
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"error": "Username already exists"}), 400

        user.username = data["username"]

    if data.get("email"):
        user.email = data["email"]

    if data.get("role"):
        user.role = data["role"]

    # Save changes
    db.session.commit()

    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "message": "User updated successfully",
        }
    )


@admin_bp.route("/api/users/<int:user_id>/reset-password", methods=["POST"])
@admin_required
def reset_user_password_api(user_id):
    """Reset a user's password."""
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    if not data.get("new_password"):
        return jsonify({"error": "New password is required"}), 400

    # Update password
    user.set_password(data["new_password"])  # Use the User model's method

    # Set force_password_change flag if requested
    if data.get("force_password_change"):
        user.force_password_change = True

    # Save changes
    db.session.commit()

    return jsonify({"message": "Password reset successfully"})


@admin_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user_api(user_id):
    """Delete a user."""
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Don't allow deleting the last admin user
    if hasattr(user, "role") and user.role == "admin":
        admin_count = User.query.filter_by(role="admin").count()
        if admin_count <= 1:
            return jsonify({"error": "Cannot delete the last admin user"}), 400

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"})


@admin_bp.route("/api/system/logs", methods=["GET"])
@admin_required
def get_system_logs_api():
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
def get_system_info_api():
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

        system_info.update(
            {
                "cpu_count": psutil.cpu_count(),
                "memory_total": round(
                    psutil.virtual_memory().total / (1024 * 1024 * 1024), 2
                ),  # GB
                "memory_available": round(
                    psutil.virtual_memory().available / (1024 * 1024 * 1024), 2
                ),  # GB
                "disk_total": round(
                    psutil.disk_usage("/").total / (1024 * 1024 * 1024), 2
                ),  # GB
                "disk_free": round(
                    psutil.disk_usage("/").free / (1024 * 1024 * 1024), 2
                ),  # GB
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            }
        )
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
def diagnostics_test_api():
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
