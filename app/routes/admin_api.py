"""
Admin API routes for the CultivAR application.
"""

from flask import jsonify, request, session
from app.models.base_models import User, db
# Removed unused hash_password import
import datetime

def register_admin_api_routes(app):
    """
    Register admin API routes.

    Args:
        app: The Flask application.
    """

    # Helper function to check admin authentication
    def admin_required(f):
        def decorated_function(*args, **kwargs):
            if not session.get('admin'):
                return jsonify({'error': 'Admin login required'}), 401
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

    @app.route('/api/admin/users', methods=['GET'])
    @admin_required
    def get_users_api():
        """Get all users."""
        users = User.query.all()

        # Convert users to a list of dictionaries
        user_list = []
        for user in users:
            user_dict = {
                'id': user.id,
                'username': user.username,
                'email': user.email if hasattr(user, 'email') else '',
                'role': user.role if hasattr(user, 'role') else 'user',
                'is_active': True,  # In a real app, you'd check a status field
                'last_login': user.last_login.isoformat() if hasattr(user, 'last_login') and user.last_login else None
            }
            user_list.append(user_dict)

        return jsonify(user_list)

    @app.route('/api/admin/users', methods=['POST'])
    @admin_required
    def add_user_api():
        """Add a new user."""
        data = request.json

        # Validate required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400

        # Check if username already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        # Create new user
        new_user = User(username=data['username'])
        new_user.set_password(data['password']) # Use the User model's method

        # Add optional fields
        if data.get('email'):
            new_user.email = data['email']

        if data.get('role'):
            new_user.role = data['role']

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id': new_user.id,
            'username': new_user.username,
            'message': 'User created successfully'
        }), 201

    @app.route('/api/admin/users/<int:user_id>', methods=['GET'])
    @admin_required
    def get_user_api(user_id):
        """Get a user by ID."""
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_dict = {
            'id': user.id,
            'username': user.username,
            'email': user.email if hasattr(user, 'email') else '',
            'role': user.role if hasattr(user, 'role') else 'user',
            'is_active': True,  # In a real app, you'd check a status field
            'last_login': user.last_login.isoformat() if hasattr(user, 'last_login') and user.last_login else None
        }

        return jsonify(user_dict)

    @app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
    @admin_required
    def update_user_api(user_id):
        """Update a user."""
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.json

        # Update fields
        if data.get('username'):
            # Check if username already exists for another user
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({'error': 'Username already exists'}), 400

            user.username = data['username']

        if data.get('email'):
            user.email = data['email']

        if data.get('role'):
            user.role = data['role']

        # Save changes
        db.session.commit()

        return jsonify({
            'id': user.id,
            'username': user.username,
            'message': 'User updated successfully'
        })

    @app.route('/api/admin/users/<int:user_id>/reset-password', methods=['POST'])
    @admin_required
    def reset_user_password_api(user_id):
        """Reset a user's password."""
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.json

        if not data.get('new_password'):
            return jsonify({'error': 'New password is required'}), 400

        # Update password
        user.set_password(data['new_password']) # Use the User model's method

        # Set force_password_change flag if requested
        if data.get('force_password_change'):
            user.force_password_change = True

        # Save changes
        db.session.commit()

        return jsonify({
            'message': 'Password reset successfully'
        })

    @app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
    @admin_required
    def delete_user_api(user_id):
        """Delete a user."""
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Don't allow deleting the last admin user
        if hasattr(user, 'role') and user.role == 'admin':
            admin_count = User.query.filter_by(role='admin').count()
            if admin_count <= 1:
                return jsonify({'error': 'Cannot delete the last admin user'}), 400

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'message': 'User deleted successfully'
        })

    @app.route('/api/admin/system/logs', methods=['GET'])
    @admin_required
    def get_system_logs_api():
        """Get system logs."""
        # In a real application, this would read from a log file
        # For now, we'll return some sample logs
        logs = [
            {'timestamp': datetime.datetime.now().isoformat(), 'level': 'INFO', 'message': 'Application started'},
            {'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat(), 'level': 'INFO', 'message': 'User login: admin'},
            {'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=10)).isoformat(), 'level': 'ERROR', 'message': 'Database connection failed'},
            {'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=11)).isoformat(), 'level': 'INFO', 'message': 'Database connection restored'},
            {'timestamp': (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat(), 'level': 'WARN', 'message': 'High temperature detected: 85.2°F'}
        ]

        return jsonify(logs)

    @app.route('/api/admin/system/info', methods=['GET'])
    @admin_required
    def get_system_info_api():
        """Get system information."""
        import sys
        import platform
        import os

        # System info
        system_info = {
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'os_name': platform.system(),
            'os_version': platform.version()
        }

        # Try to get additional system info using psutil if available
        try:
            import psutil
            system_info.update({
                'cpu_count': psutil.cpu_count(),
                'memory_total': round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2),  # GB
                'memory_available': round(psutil.virtual_memory().available / (1024 * 1024 * 1024), 2),  # GB
                'disk_total': round(psutil.disk_usage('/').total / (1024 * 1024 * 1024), 2),  # GB
                'disk_free': round(psutil.disk_usage('/').free / (1024 * 1024 * 1024), 2),  # GB
                'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat()
            })
        except ImportError:
            # psutil not available, add some basic info
            system_info.update({
                'cpu_count': 'N/A',
                'memory_total': 'N/A',
                'memory_available': 'N/A',
                'disk_total': 'N/A',
                'disk_free': 'N/A',
                'boot_time': 'N/A'
            })

        return jsonify(system_info)

    @app.route('/api/admin/diagnostics/test', methods=['GET'])
    def diagnostics_test_api():
        """A simple endpoint for testing the diagnostics functionality."""
        import time
        import random

        # Simulate a delay
        time.sleep(0.5)

        # Return a test response
        return jsonify({
            'success': True,
            'message': 'Diagnostics test successful',
            'timestamp': time.time(),
            'random_value': random.random(),
            'test_array': [1, 2, 3, 4, 5],
            'test_object': {
                'name': 'Test Object',
                'type': 'Diagnostics',
                'enabled': True
            }
        })
