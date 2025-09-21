#!/usr/bin/env python3
"""
Password Update Test Script
Tests the actual password update process as done by the admin interface.
"""

import sys
import os
import traceback

# Add app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_password_update():
    """Test the password update functionality that's failing in the admin interface."""

    print("=" * 80)
    print("PASSWORD UPDATE SIMULATION - Like Admin Interface")
    print("=" * 80)

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

            # Check existing users
            print("DEBUG: Querying existing users...")
            existing_users = User.query.all()
            print(f"DEBUG: Found {len(existing_users)} users:")

            for user in existing_users:
                print(f"  - ID: {user.id}, Username: {user.username}, Is Admin: {user.is_admin}")
                if user.username == "isley":
                    print(f"  🎯 FOUND TARGET: User 'isley' with ID {user.id}")

            # Find the admin user
            admin_user = None
            for user in existing_users:
                if user.is_admin:  # Look for first admin user
                    admin_user = user
                    break

            if not admin_user:
                print("ERROR: No admin user found!")
                return False

            print(f"DEBUG: Found admin user: {admin_user.username} (ID: {admin_user.id})")

            # Test EXACTLY what the admin interface is doing
            print("\nDEBUG: Testing password update simulation...")

            # Step 1: Get user by ID (this is where session.get() is failing)
            print("STEP 1: Getting user by ID...")
            try:
                # Try the NEW SQLAlchemy 2.0 way first
                print("  - Trying SQLAlchemy 2.0+ Session.get() syntax...")
                target_user = db.session.get(User, ident=admin_user.id)
                if target_user:
                    print("  ✅ SUCCESS: User found using modern syntax"                    print(f"  - Found user: {target_user.username} (ID: {target_user.id})")
                else:
                    print("  ❌ FAILED: User not found using modern syntax"
            except Exception as e:
                print.f(f"  ❌ ERROR with modern syntax: {e}")
                print("  💡 NOTE: This confirms the SQLAlchemy 2.0 compatibility issue")

            # Step 2: Update password if user found
            if 'target_user' in locals() and target_user:
                print("\nSTEP 2: Updating password...")
                try:
                    old_hash = target_user.password_hash[:10] + "..."
                    print(f"  - Old password hash: {old_hash}")

                    # Generate new password hash
                    new_password_hash = generate_password_hash("1238")
                    print(f"  - New password hash generated: {new_password_hash[:10]}...")

                    # Update user
                    target_user.password_hash = new_password_hash
                    target_user.updated_at = None  # Will be set to current time
                    print("  - User object updated successfully"
                    # Commit changes
                    db.session.commit()
                    print("  ✅ SUCCESS: Password update committed to database"
                    # Verify
                    updated_user = User.query.get(admin_user.id)
                    if updated_user:
                        print("  ✅ VERIFICATION: User found after update"                        print(f"  - Password hash: {updated_user.password_hash[:10]}...")
                        print("  - Updated timestamp: Available"
                        print("  🎉 PASSWORD UPDATE SUCCESSFUL!"
                        return True
                    else:
                        print("  ❌ VERIFICATION FAILED: User not found after update"
                except Exception as e:
                    print(f"  ❌ ERROR updating password: {e}")
                    traceback.print_exc()
                    db.session.rollback()

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        traceback.print_exc()

    return False

if __name__ == '__main__':
    test_password_update()
