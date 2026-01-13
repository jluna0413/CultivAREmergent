"""
Diagnostics blueprint for the CultivAR application.
"""
import os
import platform
import sys

from flask import Blueprint, current_app, jsonify
from flask_login import login_required, current_user

from app.models import db

diagnostics_bp = Blueprint("diagnostics", __name__)


@diagnostics_bp.route("/diagnostics")
@login_required
def diagnostics():
    """Get system diagnostics information. Requires admin authentication."""
    # Require admin privileges for sensitive system information
    if not current_user.is_admin:
        return jsonify({"error": "Admin privileges required"}), 403
    # App info
    info = {
        "app_name": "CultivAR",
        "version": getattr(current_app, "version", "unknown"),
        "environment": os.getenv("FLASK_ENV", "production"),
        "python_version": sys.version,
        "platform": platform.platform(),
        "cwd": os.getcwd(),
    }

    # Database check
    try:
        from sqlalchemy import text

        db.session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e}"

    # Recent log lines
    log_path = os.path.join(os.getcwd(), "logs", "cultivar.log")
    try:
        with open(log_path, "r") as f:
            log_lines = f.readlines()[-20:]
    except Exception as e:
        log_lines = [f"Could not read log: {e}"]

    return jsonify({"info": info, "database": db_status, "recent_logs": log_lines})
