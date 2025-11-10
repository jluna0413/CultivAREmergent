"""
CultivAR Application Factory
This file contains the application factory for creating the Flask app instance.
"""

import os
import sys
import ssl
from datetime import datetime, timedelta
from flask import Flask, request, g, redirect, url_for
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_limiter.errors import RateLimitExceeded
from app.utils.rate_limiter import limiter
from app.config.config import Config
from app.database import db
from app.models.base_models import User, Plant, Cultivar, Status, Zone, Breeder
from app.models.acinfinity_models import ACInfinityDevice, ACInfinityToken
from app.models.ecowitt_models import EcowittDevice
from app.models.system_models import SystemActivity
from werkzeug.security import generate_password_hash
from app.routes import register_routes
from app.blueprints.auth import auth_bp
from app.blueprints.dashboard import dashboard_bp
from app.blueprints.cultivars import cultivars_bp
from app.blueprints.breeders import breeders_bp
from app.blueprints.admin import admin_bp
from app.blueprints.clones import clones_bp
from app.blueprints.diagnostics import diagnostics_bp
from app.blueprints.market import market_bp
from app.blueprints.marketing import (
    marketing_bp as marketing_blueprint, # Renamed to avoid conflict
    marketing_home,
    blog,
    blog_post,
    waitlist,
    waitlist_success,
    download_lead_magnet,
    waitlist_stats,
    search_blog,
)
from app.blueprints.newsletter import newsletter_bp
from app.blueprints.social import social_bp
from app.logger import logger
from flask_wtf.csrf import CSRFProtect, generate_csrf

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
    # Ensure SECRET_KEY is set. In development provide a safe fallback so
    # sessions, flashes and CSRF work during local testing. Do NOT use the
    # fallback in production.
    secret_key = Config.SECRET_KEY
    if not secret_key:
        # When running in debug/dev mode, allow a predictable dev key so
        # tests and local runs don't fail due to missing SECRET_KEY.
        if Config.DEBUG:
            secret_key = os.getenv('DEV_SECRET_KEY', 'dev-secret-key-for-local-testing')
            print('WARNING: No SECRET_KEY set — using development fallback. Do not use in production.')
        else:
            raise ValueError('SECRET_KEY must be set in production environment.')
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
    
    # Ensure upload folder exists
    Config.ensure_upload_folder()
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        # SQLAlchemy Session.get expects (Model, primary_key). Ensure we pass an int id.
        try:
            return db.session.get(User, int(user_id))
        except Exception:
            return None

    # Configure Flask session settings
    app.config['SESSION_COOKIE_SECURE'] = not app.config.get('DEBUG', False)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # 24 hours

    # Configure Flask-Talisman for enterprise-grade security headers
    # Adjust security settings based on environment
    # Use the configured DEBUG value from Config rather than forcing True
    app.config['DEBUG'] = getattr(Config, 'DEBUG', False)
    is_production = not app.config.get('DEBUG', False)

    # Use different Talisman configurations for production vs development
    if is_production:
        # Production: Enable HTTPS redirects and full security
        talisman = Talisman(
            app,
            content_security_policy={
                'default-src': "'self'",
                'script-src': "'self'",
                'style-src': "'self' 'unsafe-inline'",
                'style-src-attr': "'unsafe-inline'",
                'img-src': "'self' data: https:",
                'font-src': "'self' data:",
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
        print("DEBUG: Talisman initialized with force_https redirect")
    else:
        # In development, use minimal security headers without HTTPS redirects
        talisman = Talisman(
            app,
            content_security_policy={
                'default-src': "'self'",
                'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
                'style-src': "'self' 'unsafe-inline'",
                'style-src-attr': "'unsafe-inline'",
                'img-src': "'self' data: http: https:",
                'font-src': "'self' data:",
                'connect-src': "'self' data:",
                'frame-src': "'none'",
                'object-src': "'none'",
                'base-uri': "'self'",
                'form-action': "'self'",
            },
            content_security_policy_nonce_in=['script-src', 'style-src'],
            strict_transport_security=False,
            strict_transport_security_max_age=0,
            strict_transport_security_include_subdomains=False,
            strict_transport_security_preload=False,
            session_cookie_secure=False,
            session_cookie_http_only=True,
            force_https=False,  # Disable HTTPS redirect for development
            force_https_permanent=False,
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
        print("DEBUG: Talisman initialized without force_https redirect for development")

    # Initialize Flask-Limiter for DDoS protection
    # Support both Flask-Limiter and slowapi limiter compatibility (slowapi Limiter may not expose init_app)
    try:
        if hasattr(limiter, 'init_app'):
            limiter.init_app(app)
        else:
            # attach limiter instance to app.extensions for potential usage by code expecting an extension
            app.extensions = getattr(app, 'extensions', {})
            app.extensions['limiter'] = limiter
    except Exception:
        # If any unexpected error occurs initializing the limiter, continue without failing app creation
        pass

    # Enable CSRF protection for forms and POST endpoints
    try:
        if not app.config.get('DEBUG', False):
            CSRFProtect(app)
        app.config['WTF_CSRF_TIME_LIMIT'] = None

        # Expose csrf_token() helper to Jinja templates
        @app.context_processor
        def inject_csrf_token():  # type: ignore
            try:
                return dict(csrf_token=generate_csrf)
            except Exception:
                return {}
    except Exception as _:
        # If Flask-WTF not available, skip without crashing in dev
        @app.context_processor
        def inject_csrf_token_missing():  # type: ignore
            return {}

    @app.errorhandler(RateLimitExceeded)
    def rate_limit_exceeded(e):
        return "Too many requests. Please try again later.", 429

    # Create database tables and initialize data
    with app.app_context():
        try:
            from app.models import migrate_db, init_db
            
            # Create tables and migrate schema
            migrate_db()
            
            # Initialize default data
            init_db()            
            
            # Create a test plant for clone demonstration if no plants exist
            if Plant.query.count() == 0:
                # Create a test breeder
                test_breeder = Breeder.query.filter_by(name='CultivAR Seeds').first()
                if not test_breeder:
                    test_breeder = Breeder()
                    test_breeder.name = 'CultivAR Seeds'
                    db.session.add(test_breeder)
                    db.session.flush()
                
                # Create a test strain
                test_cultivar = Cultivar.query.filter_by(name='Green Goddess').first()
                if not test_cultivar:
                    test_cultivar = Cultivar(
                        name='Green Goddess',
                        breeder_id=test_breeder.id,
                        indica=60,
                        sativa=40,
                        description='Premium hybrid strain perfect for cloning',
                        seed_count=10,
                        cycle_time=75
                    )
                    db.session.add(test_cultivar)
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
                    cultivar_id=test_cultivar.id,
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
    register_routes(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    # Legacy import removed - strains blueprint now part of cultivars
    # from app.blueprints.strains import strains_bp
    # Blueprint registration removed - strains routes now part of cultivars
    # app.register_blueprint(strains_bp)
    app.register_blueprint(cultivars_bp, url_prefix='/cultivars')
    app.register_blueprint(breeders_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(clones_bp)
    app.register_blueprint(diagnostics_bp)
    app.register_blueprint(market_bp)

    # Register marketing blueprints
    app.register_blueprint(marketing_blueprint)

    # Expose the marketing homepage at top-level paths for nicer URLs
    # e.g. /home/ or /site/ will render the same content as /marketing/
    try:
        # Register only /site/ to avoid colliding with existing 'home' endpoint
        app.add_url_rule('/site/', endpoint='site', view_func=marketing_home)
    except RuntimeError:
        # In some contexts (import-time before app ready) add_url_rule may fail;
        # it's safe to ignore here because blueprint route still exists at /marketing/.
        pass

    # Also expose common marketing endpoints under /site/... for nicer canonical URLs
    try:
        app.add_url_rule('/site/blog/', endpoint='site_blog', view_func=blog)
        app.add_url_rule('/site/blog/<slug>', endpoint='site_blog_post', view_func=blog_post)
        app.add_url_rule('/site/waitlist', endpoint='site_waitlist', view_func=waitlist)
        app.add_url_rule('/site/waitlist/success/<code>', endpoint='site_waitlist_success', view_func=waitlist_success)
        app.add_url_rule('/site/download/<magnet_name>', endpoint='site_download', view_func=download_lead_magnet)
        app.add_url_rule('/site/api/waitlist/stats', endpoint='site_api_waitlist_stats', view_func=waitlist_stats)
        app.add_url_rule('/site/api/blog/search', endpoint='site_api_blog_search', view_func=search_blog)
    except RuntimeError:
        # ignore if app isn't fully wired yet
        pass

    # Add a safe, non-destructive redirect from the legacy /marketing/ URL to /site/
    # This lets users continue to use old bookmarks while surfacing the new path.
    def _marketing_redirect():
        return redirect(url_for('site'))

    try:
        app.add_url_rule('/marketing/', endpoint='marketing_redirect', view_func=_marketing_redirect)
        app.add_url_rule('/marketing', endpoint='marketing_redirect_noslash', view_func=_marketing_redirect)
    except RuntimeError:
        # ignore if app isn't fully wired yet
        pass
    app.register_blueprint(newsletter_bp)
    app.register_blueprint(social_bp)
    
    # Initialize logger
    logger.info("CultivAR application created successfully")

    # Template context processor: ensure csp_nonce is available in templates
    @app.context_processor
    def inject_csp_nonce():
        """Provide a defensive way to expose the CSP nonce to templates as `csp_nonce`.

        Flask-Talisman normally exposes `csp_nonce` to templates when
        `content_security_policy_nonce_in` is configured. In case that
        behavior differs across versions or environments, try common
        locations (flask.g, request attributes, or the extension) and
        return None if not found.
        """
        try:
            nonce = None
            # common places Talisman might store it
            nonce = getattr(g, 'csp_nonce', None)
            if not nonce:
                nonce = getattr(request, 'csp_nonce', None)

            # try to read from the talisman extension if present
            if not nonce:
                tal = app.extensions.get('talisman') if hasattr(app, 'extensions') else None
                if tal:
                    # Some versions store a callable or attribute for nonce
                    candidate = getattr(tal, 'csp_nonce', None) or getattr(tal, '_csp_nonce', None)
                    if callable(candidate):
                        try:
                            nonce = candidate()
                        except Exception:
                            nonce = None
                    else:
                        nonce = candidate

            return {'csp_nonce': nonce}
        except Exception:
            return {'csp_nonce': None}
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('CULTIVAR_PORT', 5000))

    # For development testing, run on HTTP only to avoid SSL issues
    print("DEBUG: Running Flask app on HTTP only for development testing")
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG, use_reloader=True)
