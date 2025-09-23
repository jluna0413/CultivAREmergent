#!/usr/bin/env python3
"""
Simple test Flask app without Talisman to isolate HTTPS redirect issue
"""

import os
import sys

# Add app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def create_test_app():
    """Create basic Flask app without Talisman"""
    from flask import Flask
    from flask_login import LoginManager
    from typing import Any, cast

    app = Flask(__name__,
                template_folder='app/web/templates',
                static_folder='app/web/static')

    # Load configuration
    from app.config.config import Config
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    from app.models import db
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    cast(Any, login_manager).login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.base_models import User
        return db.session.get(User, int(user_id))

    # Simple test route
    @app.route('/test')
    def test():
        return "Hello from HTTP server!"

    @app.route('/admin/users/<int:user_id>/edit')
    def admin_edit(user_id):
        return f"Edit user {user_id}"

    # Basic database init
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_test_app()

    # Force HTTP without SSL for testing
    port = int(os.getenv('CULTIVAR_PORT', 5000))
    print("Starting test app on HTTP (no HTTPS redirect)...")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
