#!/usr/bin/env python3
"""
Simple debugging script to isolate Session.get() error
"""

import sys
import os

# Add app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_session_get():
    """Test the specific Session.get() call that's causing issues"""

    print("=== SESSION.GET() DEBUG TEST ===")

    try:
        from flask import Flask
        from app.models import db
        from app.models.base_models import User

        # Create app
        app = Flask(__name__,
                    template_folder='app/web/templates',
                    static_folder='app/web/static')

        from app.config.config import Config
        app.config['SECRET_KEY'] = Config.SECRET_KEY
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)

        with app.app_context():
            print("DEBUG: App context established")

            # Get admin user
            admin_user = None
            users = User.query.all()
            for user in users:
                if user.is_admin:
                    admin_user = user
                    break

            if not admin_user:
                print("ERROR: No admin user found")
                return False

            print(".2f")

            # TEST THE SPECIFIC METHOD THAT'S FAILING
            print("\n=== TESTING SESSION.GET() CALL ===")

            # This is the exact call that's causing the error
            try:
                print("SQLAlchemy Version info:")
                import sqlalchemy
                print(f"Version: {sqlalchemy.__version__}")

                print("Testing db.session.get(User, ident=1)"                result = db.session.get(User, ident=admin_user.id)
                if result:
                    print(f"SUCCESS: Got user {result.username}")
                    return True
                else:
                    print("FAILURE: Got None result")
                    return False
            except TypeError as e:
                print(f"TYPE ERROR: {e}")
                print("This suggests the method signature is incompatible!")

                # Try alternative approaches
                print("\nTrying alternative syntax...")
                try:
                    result = db.session.get(User, admin_user.id)  # No 'ident'
                    if result:
                        print(f"SUCCESS: Alternative syntax worked - got {result.username}")
                        return True
                    else:
                        print("FAILURE: Alternative syntax returned None")
                        return False
                except Exception as e2:
                    print(f"FAILURE: Alternative syntax also failed: {e2}")
                    return False

            except Exception as e:
                print(f"UNEXPECTED ERROR: {e}")
                import traceback
                traceback.print_exc()
                return False

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_session_get()
    if success:
        print("\n✅ Session.get() works correctly!")
    else:
        print("\n❌ Session.get() has issues - check logs above")
