#!/usr/bin/env python3
"""
Debug Password Update Issue
This script will help us isolate exactly where the Session.get() error is occurring.
"""

import sys
import os
import traceback

# Add app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def simulate_password_update(user_id, new_password):
    """Simulate the password update process step by step."""

    print("=" * 60)
    print(f"DEBUG: Starting password update simulation for user_id: {user_id}")
    print(f"DEBUG: New password: {new_password[:3]}...")
    print("=" * 60)

    try:
        # Import necessary modules
        print("DEBUG: Importing Flask modules...")
        from flask import Flask
        from werkzeug.security import generate_password_hash

        # Import app models
        print("DEBUG: Importing database models...")
        from app.models import db
        from app.models.base_models import User

        # Create Flask app
        print("DEBUG: Creating Flask app...")
        app = Flask(__name__,
                    template_folder='app/web/templates',
                    static_folder='app/web/static')

        # Load configuration
        print("DEBUG: Loading configuration...")
        from app.config.config import Config
        app.config['SECRET_KEY'] = Config.SECRET_KEY
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialize database
        print("DEBUG: Initializing database...")
        db.init_app(app)

        with app.app_context():
            print("DEBUG: Inside application context")

            # Check current users
            print("DEBUG: Querying all users...")
            all_users = User.query.all()
            print(f"DEBUG: Found {len(all_users)} users:")

            for user in all_users:
                print(f"  - ID: {user.id}, Username: {user.username}, Is Admin: {user.is_admin}")

            # Try to get the specific user
            print(f"DEBUG: Looking up user with ID {user_id}")
            print("DEBUG: Using db.session.get(User, user_id)...")

            try:
                user = db.session.get(User, ident=user_id)
                print(f"DEBUG: User lookup successful: {user}")
            except Exception as e:
                print(f"ERROR: Failed to get user - {e}")
                print(f"ERROR: Exception type: {type(e)}")
                traceback.print_exc()
                return False

            if not user:
                print(f"ERROR: No user found with ID {user_id}")
                return False

            print(f"DEBUG: Found user: ID={user.id}, Username={user.username}")

            # Try to update the password
            print("DEBUG: Updating password...")
            try:
                user.password_hash = generate_password_hash(new_password)
                from datetime import datetime
                user.updated_at = datetime.now()
                print(f"DEBUG: Password hash generated: {user.password_hash[:10]}...")
                print(f"DEBUG: User updated_at set: {user.updated_at}")
            except Exception as e:
                print(f"ERROR: Failed to update user object - {e}")
                traceback.print_exc()
                return False

            # Try to commit
            print("DEBUG: Committing changes to database...")
            try:
                db.session.commit()
                print("DEBUG: Commit successful!")
            except Exception as e:
                print(f"ERROR: Failed to commit changes - {e}")
                db.session.rollback()
                traceback.print_exc()
                return False

            # Verify the update
            print("DEBUG: Verifying the update...")
            try:
                updated_user = db.session.get(User, ident=user_id)
                print(f"DEBUG: Verification successful: {updated_user.username}")
                print(f"DEBUG: Password hash length: {len(updated_user.password_hash)}")
            except Exception as e:
                print(f"ERROR: Failed to verify update - {e}")
                traceback.print_exc()
                return False

            print("SUCCESS: Password update completed successfully!")
            return True

    except ImportError as e:
        print(f"ERROR: Import failed - {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"ERROR: Unexpected error - {e}")
        traceback.print_exc()

    return False

def check_sqlalchemy_version():
    """Check the SQLAlchemy version being used."""
    print("\n" + "=" * 60)
    print("DEBUG: Checking SQLAlchemy version and configuration")
    print("=" * 60)

    try:
        import sqlalchemy
        print(f"SQLAlchemy version: {sqlalchemy.__version__}")

        # Check if using Alembic
        try:
            import alembic
            print(f"Alembic version: {alembic.__version__}")
        except ImportError:
            print("Alembic not found")

        # Check Flask-SQLAlchemy
        try:
            import flask_sqlalchemy
            print(f"Flask-SQLAlchemy version: {flask_sqlalchemy.__version__}")
        except ImportError:
            print("Flask-SQLAlchemy not found")

    except Exception as e:
        print(f"Failed to check versions: {e}")

if __name__ == '__main__':
    print("=== PASSWORD UPDATE DEBUG SCRIPT ===")
    print("This script will help us isolate the Session.get() error")

    check_sqlalchemy_version()

    # Get user input
    user_id = input("Enter user ID to test password update (default: 1): ").strip()
    if not user_id:
        user_id = "1"

    user_id = int(user_id)

    # Use a simple password for testing
    test_password = "testpassword123"

    print(f"\nTesting password update for user ID {user_id}")
    simulate_password_update(user_id, test_password)
