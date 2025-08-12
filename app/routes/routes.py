"""
Route definitions for the CultivAR application.
"""

import os

from flask import (
    Flask,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_login import (
    current_user,  # Assuming Flask-Login is used/intended
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import (  # Added generate for potential future use
    check_password_hash,
    generate_password_hash,
)

from app.config.config import Config  # Corrected import path
from app.handlers import (
    breeder_handlers,
    plant_handlers,
    sensor_handlers,
    settings_handlers,
    strain_handlers,
)
from app.logger import logger  # Corrected import path for logger as well
from app.models.base_models import Plant, Sensor, Strain, Stream, User, db

# Removed: from utils.auth import check_password # Using werkzeug check_password_hash directly
from app.utils.helpers import format_date, format_datetime


def register_routes(app):
    """
    Register all routes for the application.

    Args:
        app: The Flask application.
    """
    # Register basic routes
    register_basic_routes(app)

    # Register other route modules


def register_basic_routes(app):
    """
    Register basic routes that don't require authentication.

    Args:
        app: The Flask application.
    """

    @app.route("/")
    def landing_page():
        """Render the viral landing page."""
        return render_template("landing/index.html")

    @app.route("/home")
    def home():
        """Redirect from old home to landing page."""
        return redirect(url_for("landing_page"))

    @app.route("/api/newsletter/subscribe", methods=["POST"])
    def newsletter_subscribe():
        """Handle newsletter subscription."""
        try:
            data = request.get_json()
            phone = data.get("phone", "").strip()

            if not phone or len(phone) != 10:
                return jsonify({"error": "Invalid phone number"}), 400

            # Here you would integrate with your SMS service (Twilio, etc.)
            # For now, we'll just log it
            logger.info(f"Newsletter signup: {phone}")

            # You could store in database
            # newsletter_subscriber = NewsletterSubscriber(phone=phone)
            # db.session.add(newsletter_subscriber)
            # db.session.commit()

            return jsonify(
                {"success": True, "message": "Successfully subscribed to newsletter"}
            )

        except Exception as e:
            logger.error(f"Newsletter subscription error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/health")
    def health():
        """Health check endpoint."""
        return jsonify({"status": "ok"})

    @app.route("/favicon.ico")
    def favicon():
        """Serve the favicon."""
        return send_from_directory(
            os.path.join(app.root_path, "app/web/static/images"),
            "favicon-32x32.png",
            mimetype="image/png",
        )

    @app.route("/manifest.json")
    def manifest():
        """Serve the PWA manifest file."""
        return send_from_directory(
            os.path.join(app.root_path, "app/web/static"),
            "manifest.json",
            mimetype="application/json",
        )

    @app.route("/sensors/delete/<int:sensor_id>", methods=["DELETE"])
    @login_required  # Protect API route
    def delete_sensor(sensor_id):
        """Delete a sensor."""
        result = sensor_handlers.delete_sensor(sensor_id)
        return jsonify(result)

    # Settings API routes
    @app.route("/settings", methods=["POST"])
    @login_required  # Protect API route
    def save_settings():
        """Save settings."""
        data = request.json
        result = settings_handlers.save_settings(data)
        return jsonify(result)

    @app.route("/settings/upload-logo", methods=["POST"])
    @login_required  # Protect API route
    def upload_logo():
        """Upload a logo."""
        file = request.files.get("logo")
        result = settings_handlers.upload_logo(file)
        return jsonify(result)

    # Utility routes
    @app.route("/decorateImage", methods=["POST"])
    @login_required  # Protect API route
    def decorate_image():
        """Decorate an image with text."""
        file = request.files.get("image")
        text = request.form.get("text", "")
        position = request.form.get("position", "bottom")
        from utils.image import decorate_image as decorate

        result = decorate(file, text, position=position)
        return jsonify(result)
