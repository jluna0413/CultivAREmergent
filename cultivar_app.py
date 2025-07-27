"""
CultivAR Application Factory
This file contains the application factory for creating the Flask app instance.
"""

import os
import sys
from datetime import datetime, timedelta
from flask import Flask
from flask_login import LoginManager

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
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.base_models import User
        return User.query.get(int(user_id))
    
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
            
            # Create default admin user if it doesn't exist
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(username='admin', is_admin=True)
                admin_user.password_hash = generate_password_hash('isley')  # Default password from README
                db.session.add(admin_user)
                db.session.commit()
                print("Created default admin user with username 'admin' and password 'isley'")
            elif not admin_user.is_admin:
                # Update existing admin user to have admin privileges
                admin_user.is_admin = True
                db.session.commit()
                print("Updated admin user with admin privileges")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    # Register routes
    from app.routes import register_routes
    register_routes(app)
    
    # Initialize logger
    from app.logger import logger
    logger.info("CultivAR application created successfully")
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('ISLEY_PORT', 8001))  # Changed from 4200 to 8001 for production
    app.run(host='0.0.0.0', port=port, debug=True)