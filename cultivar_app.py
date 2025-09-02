"""
CultivAR Application Factory
This file contains the application factory for creating the Flask app instance.
"""

import os
import sys
import ssl
from datetime import datetime, timedelta
from flask import Flask, request
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_limiter.errors import RateLimitExceeded
from app.utils.rate_limiter import limiter

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application.
    """
    # Create Flask app instance
    app = Flask(__name__,
                template_folder='app/web/templates',
                static_folder='app/web/static')
    
    # Load configuration
    from app.config.config import Config
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
    
    # Ensure upload folder exists
    Config.ensure_upload_folder()
    
    # Initialize database
    from app.models import db
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.base_models import User
        return db.session.get(User, int(user_id))

    # Configure Flask session settings
    app.config['SESSION_COOKIE_SECURE'] = not app.config.get('DEBUG', False)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # 24 hours

    # Configure Flask-Talisman for enterprise-grade security headers
    # Adjust security settings based on environment
    is_production = not app.config.get('DEBUG', False)

    talisman = Talisman(
        app,
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
            'style-src': "'self' 'unsafe-inline'",
            'img-src': "'self' data: https:",
            'font-src': "'self'",
            'connect-src': "'self'",
            'frame-src': "'none'",
            'object-src': "'none'",
            'base-uri': "'self'",
            'form-action': "'self'",
        },
        content_security_policy_nonce_in=['script-src', 'style-src'],
        strict_transport_security=is_production,
        strict_transport_security_max_age=31536000,  # 1 year
        strict_transport_security_include_subdomains=is_production,
        strict_transport_security_preload=is_production,
        session_cookie_secure=is_production,
        session_cookie_http_only=True,
        force_https=is_production,
        force_https_permanent=is_production,
        force_file_save=False,
        frame_options='DENY',
        x_content_type_options='nosniff',
        referrer_policy='strict-origin-when-cross-origin',
        permissions_policy={
            'geolocation': (),
            'camera': (),
            'microphone': (),
            'payment': (),
            'usb': (),
        }
    )

    # Initialize Flask-Limiter for DDoS protection
    limiter.init_app(app)

    @app.errorhandler(RateLimitExceeded)
    def rate_limit_exceeded(e):
        return "Too many requests. Please try again later.", 429

    # Create database tables and initialize data
    with app.app_context():
        try:
            from app.models import migrate_db, init_db
            from app.models.base_models import User
            from app.models.acinfinity_models import ACInfinityDevice, ACInfinityToken
            from app.models.ecowitt_models import EcowittDevice
            from app.models.system_models import SystemActivity
            from werkzeug.security import generate_password_hash
            
            # Create tables
            db.create_all()
            
            # Initialize default data
            init_db()
            
            
            # Create a test plant for clone demonstration if no plants exist
            from app.models.base_models import Plant, Strain, Status, Zone, Breeder
            if Plant.query.count() == 0:
                # Create a test breeder
                test_breeder = Breeder.query.filter_by(name='CultivAR Seeds').first()
                if not test_breeder:
                    test_breeder = Breeder(name='CultivAR Seeds')
                    db.session.add(test_breeder)
                    db.session.flush()
                
                # Create a test strain
                test_strain = Strain.query.filter_by(name='Green Goddess').first()
                if not test_strain:
                    test_strain = Strain(
                        name='Green Goddess',
                        breeder_id=test_breeder.id,
                        indica=60,
                        sativa=40,
                        description='Premium hybrid strain perfect for cloning',
                        seed_count=10,
                        cycle_time=75
                    )
                    db.session.add(test_strain)
                    db.session.flush()
                
                # Create a test zone
                test_zone = Zone.query.filter_by(name='Grow Tent 1').first()
                if not test_zone:
                    test_zone = Zone(name='Grow Tent 1')
                    db.session.add(test_zone)
                    db.session.flush()
                
                # Create a test plant
                test_plant = Plant(
                    name='Mother Plant Alpha',
                    description='Healthy mother plant ready for cloning',
                    strain_id=test_strain.id,
                    zone_id=test_zone.id,
                    status_id=2,  # Vegetative
                    is_clone=False,
                    start_dt=datetime.now() - timedelta(days=45),
                    current_week=7,
                    current_day=3
                )
                db.session.add(test_plant)
                db.session.commit()
                print("Created test plant 'Mother Plant Alpha' for clone demonstration")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    # Register routes
    from app.routes import register_routes
    register_routes(app)

    # Register blueprints
    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.blueprints.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)
    from app.blueprints.strains import strains_bp
    app.register_blueprint(strains_bp)
    from app.blueprints.breeders import breeders_bp
    app.register_blueprint(breeders_bp)
    from app.blueprints.admin import admin_bp
    app.register_blueprint(admin_bp)
    from app.blueprints.clones import clones_bp
    app.register_blueprint(clones_bp)
    from app.blueprints.diagnostics import diagnostics_bp
    app.register_blueprint(diagnostics_bp)
    from app.blueprints.market import market_bp
    app.register_blueprint(market_bp)
    
    # Initialize logger
    from app.logger import logger
    logger.info("CultivAR application created successfully")
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('CULTIVAR_PORT', 5000))

    # SSL Configuration for development/production
    from app.config.config import Config
    if Config.SSL_ENABLED and os.path.exists(Config.SSL_CERT_PATH) and os.path.exists(Config.SSL_KEY_PATH):
        # Create SSL context for HTTPS
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=Config.SSL_CERT_PATH, keyfile=Config.SSL_KEY_PATH)
        # Run with SSL in production
        app.run(host='0.0.0.0', port=port, debug=Config.DEBUG, use_reloader=False, ssl_context=ssl_context)
    else:
        # Run without SSL for development
        app.run(host='0.0.0.0', port=port, debug=Config.DEBUG, use_reloader=False)