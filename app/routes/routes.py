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

    # Register other route modules
    from app.routes.strain_routes import register_strain_routes
    register_strain_routes(app)
    
    from app.routes.user_routes import register_user_management_routes
    register_user_management_routes(app)
    
    from app.routes.export_routes import register_export_routes
    register_export_routes(app)
    
    from app.routes.clone_routes import register_clone_routes
    register_clone_routes(app)

    # Register dashboard routes
    register_dashboard_routes(app)

def register_dashboard_routes(app):
    """Register dashboard-specific routes."""
    
    @app.route('/dashboard')
    @login_required
    def protected_dashboard():
        """Render the mobile-responsive dashboard."""
        return render_template('views/index.html', title='Dashboard')

    @app.route('/dashboard-new')
    @login_required
    def dashboard_new():
        """Test route for new dashboard."""
        return render_template('views/dashboard_mobile.html', title='Dashboard')

    @app.route('/market/seed-bank')
    @login_required
    def market_seed_bank():
        """Render the seed bank page."""
        return render_template('views/market/seed_bank.html', title='Seed Bank')

    @app.route('/market/extensions')
    @login_required
    def market_extensions():
        """Render the extensions page."""
        return render_template('views/market/extensions.html', title='Extensions')

    @app.route('/market/gear')
    @login_required
    def market_gear():
        """Render the gear page."""
        return render_template('views/market/gear.html', title='Grow Gear')

    @app.route('/sensors')
    @login_required
    def sensors():
        """Render the sensors page."""
        return render_template('views/sensors.html', title='Sensors')

    @app.route('/settings')
    @login_required
    def settings():
        """Render the settings page."""
        # Create a default settings object for the template
        default_settings = {
            'accent_color': '#4CAF50',
            'email_address': '',
            'polling_interval': 60,
            'data_retention': 30,
            'acinfinity_username': '',
            'acinfinity_password': '',
            'ecowitt_api_key': '',
            'ecowitt_application_key': '',
            'ecowitt_mac': '',
            'backup_time': '02:00',
            'backup_retention': 7,
            'backup_location': './backups'
        }
        return render_template('views/settings.html', title='Settings', settings=default_settings)

    @app.route('/strains')
    @login_required
    def strains():
        """Render the strains page."""
        return render_template('views/strains.html', title='Strain Collection')

    @app.route('/plants')
    @login_required
    def plants():
        """Render the plants page."""
        return render_template('views/plants.html', title='My Plants')


def register_basic_routes(app):
    @app.route('/')
    def index():
        # Redirect to signup or dashboard as appropriate
        if current_user.is_authenticated:
            return redirect(url_for('protected_dashboard'))
        return redirect(url_for('signup'))  # Changed from 'login' to 'signup'
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

    @app.route('/manifest.json')
    def manifest():
        """Serve the PWA manifest file."""
        return send_from_directory(os.path.join(app.root_path, 'app/web/static'), 'manifest.json', mimetype='application/json')

def register_auth_routes(app):
    """
    Register authentication routes.

    Args:
        app: The Flask application.
    """
    
    @app.route('/debug-test')
    def debug_test():
        return "Debug route working - code changes are applied!"
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """ Handle user login. """
        logger.info("=== LOGIN ROUTE HIT ===")
        print("=== LOGIN ROUTE DEBUG ===")
        
        if current_user.is_authenticated:
            logger.info("User already authenticated. Redirecting to dashboard.")
            return redirect(url_for('protected_dashboard'))  # Corrected endpoint name

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            logger.info(f"Login attempt for username: {username}")
            logger.info(f"Password provided: {'Yes' if password else 'No'}")
            print(f"LOGIN DEBUG: username={username}, password={'***' if password else 'None'}")

            user = User.query.filter_by(username=username).first()
            logger.info(f"User found in database: {'Yes' if user else 'No'}")
            print(f"LOGIN DEBUG: User found: {'Yes' if user else 'No'}")
            
            if user:
                logger.info(f"User has password_hash: {hasattr(user, 'password_hash')}")
                logger.info(f"Password hash exists: {bool(user.password_hash) if hasattr(user, 'password_hash') else False}")
                print(f"LOGIN DEBUG: User has password_hash: {hasattr(user, 'password_hash')}")
                
                if hasattr(user, 'password_hash') and user.password_hash:
                    password_check = check_password_hash(user.password_hash, password)
                    logger.info(f"Password check result: {password_check}")
                    print(f"LOGIN DEBUG: Password check result: {password_check}")
                else:
                    logger.error("User has no password_hash")
                    print("LOGIN DEBUG: ERROR - User has no password_hash")

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
            phone = request.form.get('phone')
            email = request.form.get('email')
            password = request.form.get('password')

            # Check required fields
            if not password:
                flash('Password is required.', 'danger')
                return render_template('signup.html', title='Sign Up')

            # Check that either phone or email is provided
            if not phone and not email:
                flash('Either phone number or email address is required.', 'danger')
                return render_template('signup.html', title='Sign Up')

            # Generate username from phone or email
            if phone:
                username = f"user_{phone.replace('+', '').replace('-', '').replace(' ', '')}"
                contact_method = phone
            else:
                username = f"user_{email.split('@')[0]}"
                contact_method = email

            # Check if user already exists by contact method
            existing_user = None
            if phone:
                existing_user = User.query.filter_by(phone=phone).first()
            else:
                existing_user = User.query.filter_by(email=email).first()
                
            if existing_user:
                contact_type = "phone number" if phone else "email address"
                flash(f'An account with this {contact_type} already exists.', 'danger')
                return render_template('signup.html', title='Sign Up')

            # Ensure username is unique
            counter = 1
            original_username = username
            while User.query.filter_by(username=username).first():
                username = f"{original_username}_{counter}"
                counter += 1

            # Create new user
            new_user = User(username=username)
            new_user.password_hash = generate_password_hash(password)
            
            if phone:
                new_user.phone = phone
            if email:
                new_user.email = email
                
            db.session.add(new_user)
            db.session.commit()

            flash(f'Account created successfully! Your username is: {username}', 'success')
            return redirect(url_for('login'))

        return render_template('signup.html', title='Sign Up')

    @app.route('/logout')
    @login_required
    def logout():
        """Handle user logout."""
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('login'))

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
