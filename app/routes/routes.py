"""
Route definitions for the CultivAR application.
"""

import os
from flask import render_template, redirect, url_for, request, flash, jsonify, session, abort, current_app, send_from_directory, Flask
from flask_login import login_user, logout_user, login_required, current_user # Assuming Flask-Login is used/intended
from werkzeug.security import check_password_hash, generate_password_hash # Added generate for potential future use
from app.models.base_models import User, Plant, Strain, Sensor, Stream, db
# Removed: from utils.auth import check_password # Using werkzeug check_password_hash directly
from app.utils.helpers import format_date, format_datetime
from app.handlers import plant_handlers, strain_handlers, sensor_handlers, settings_handlers, breeder_handlers
from app.config import Config # Corrected import path
from app.logger import logger # Corrected import path for logger as well

def register_routes(app):
    """
    Register all routes for the application.

    Args:
        app: The Flask application.
    """
    # Register basic routes
    register_basic_routes(app)

    # Register authentication routes
    register_auth_routes(app)

    # Register strain routes
    from app.routes.strain_routes import register_strain_routes # Corrected import path
    register_strain_routes(app)

    @app.route('/dashboard')
    @login_required
    def protected_dashboard():
        """Render the dashboard."""
        return render_template('views/index.html', title='Dashboard')

    @app.route('/market/seed-bank')
    @login_required
    def market_seed_bank():
        """Render the seed bank page."""
        return render_template('views/market/seed_bank.html', title='Seed Bank')


def register_basic_routes(app):
    @app.route('/')
    def index():
        # Redirect to login or dashboard as appropriate
        if current_user.is_authenticated:
            return redirect(url_for('protected_dashboard'))
        return redirect(url_for('login'))
    """
    Register basic routes that don't require authentication.

    Args:
        app: The Flask application.
    """
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({"status": "ok"})

    @app.route('/favicon.ico')
    def favicon():
        """Serve the favicon."""
        return send_from_directory(os.path.join(app.root_path, 'app/web/static/images'), 'favicon-32x32.png', mimetype='image/png')

def register_auth_routes(app):
    """
    Register authentication routes.

    Args:
        app: The Flask application.
    """
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """ Handle user login. """
        logger.info("Login route accessed.")
        if current_user.is_authenticated:
            logger.info("User already authenticated. Redirecting to dashboard.")
            return redirect(url_for('protected_dashboard'))  # Corrected endpoint name

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            logger.info(f"Login attempt for username: {username}")

            user = User.query.filter_by(username=username).first()

            if user and hasattr(user, 'password_hash') and check_password_hash(user.password_hash, password):
                logger.info("Login successful.")
                login_user(user)  # Log the user in
                flash('Login successful!', 'success')
                # Redirect to the page the user was trying to access, or dashboard
                next_page = request.args.get('next')
                return redirect(next_page or url_for('protected_dashboard'))  # Corrected endpoint name
            else:
                logger.warning("Invalid username or password.")
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))

        return render_template('views/new_login.html', admin_login=False, title='User Login')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """Handle user signup."""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if not username or not password or not confirm_password:
                flash('All fields are required.', 'danger')
                return render_template('views/signup.html', title='Sign Up')

            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('views/signup.html', title='Sign Up')

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists.', 'danger')
                return render_template('views/signup.html', title='Sign Up')

            new_user = User(username=username)
            new_user.password_hash = generate_password_hash(password)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))

        return render_template('views/signup.html', title='Sign Up')

    @app.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        """Handle password reset request (Placeholder)."""
        # Render the auth placeholder template
        return render_template('views/auth_placeholder.html', title='Forgot Password', message='Forgot Password Page - Coming Soon!')

    @app.route('/sensors/delete/<int:sensor_id>', methods=['DELETE'])
    @login_required  # Protect API route
    def delete_sensor(sensor_id):
        """Delete a sensor."""
        result = sensor_handlers.delete_sensor(sensor_id)
        return jsonify(result)

    # Settings API routes
    @app.route('/settings', methods=['POST'])
    @login_required # Protect API route
    def save_settings():
        """Save settings."""
        data = request.json
        result = settings_handlers.save_settings(data)
        return jsonify(result)

    @app.route('/settings/upload-logo', methods=['POST'])
    @login_required # Protect API route
    def upload_logo():
        """Upload a logo."""
        file = request.files.get('logo')
        result = settings_handlers.upload_logo(file)
        return jsonify(result)

    # Utility routes
    @app.route('/decorateImage', methods=['POST'])
    @login_required # Protect API route
    def decorate_image():
        """Decorate an image with text."""
        file = request.files.get('image')
        text = request.form.get('text', '')
        position = request.form.get('position', 'bottom')
        from utils.image import decorate_image as decorate
        result = decorate(file, text, position=position)
        return jsonify(result)

    @app.route('/login/simple')
    def simple_login():
        """Render a simple login page (placeholder)."""
        return render_template('views/login.html', admin_login=False)
    @app.route('/login/auth')
    def auth_login():
        """Render the auth login page."""
        return render_template('auth/login.html', admin_login=False)

    @app.route('/login/basic')
    def basic_login():
        """Render the basic login page."""
        return render_template('views/login.html', admin_login=False)
