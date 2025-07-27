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
                    clone=False,
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
    
    # Initialize logger
    from app.logger import logger
    logger.info("CultivAR application created successfully")
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('ISLEY_PORT', 8001))  # Changed from 4200 to 8001 for production
    app.run(host='0.0.0.0', port=port, debug=True)