"""
User management handlers for the CultivAR application.
"""

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app.models import db
from app.models.base_models import User
from app.models.system_models import SystemActivity
from app.logger import logger

def get_all_users():
    """
    Get all users with their details and activity summary.
    
    Returns:
        list: List of user data dictionaries.
    """
    try:
        users = User.query.all()
        
        user_list = []
        for user in users:
            # Get user activity count
            activity_count = SystemActivity.query.filter_by(user_id=user.id).count()
            
            # Get last login (for now, we'll use updated_at as proxy)
            last_activity = SystemActivity.query.filter_by(user_id=user.id).order_by(SystemActivity.timestamp.desc()).first()
            
            user_data = {
                'id': user.id,
                'username': user.username,
                'phone': user.phone,
                'email': user.email,
                'is_admin': user.is_admin,
                'force_password_change': user.force_password_change,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None,
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None,
                'activity_count': activity_count,
                'last_activity': last_activity.timestamp.strftime('%Y-%m-%d %H:%M:%S') if last_activity else None,
                'status': 'Active' if not user.force_password_change else 'Password Reset Required'
            }
            
            user_list.append(user_data)
        
        logger.info(f"Found {len(users)} users.")
        logger.info(f"User list: {user_list}")
        return user_list
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []

def get_user_by_id(user_id):
    """
    Get a specific user by ID with detailed information.
    
    Args:
        user_id (int): The ID of the user.
        
    Returns:
        dict: User data or None if not found.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Get user activities
        activities = SystemActivity.query.filter_by(user_id=user.id).order_by(SystemActivity.timestamp.desc()).limit(10).all()
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'is_admin': user.is_admin,
            'force_password_change': user.force_password_change,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None,
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None,
            'recent_activities': [
                {
                    'type': activity.type,
                    'description': activity.description,
                    'timestamp': activity.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                } for activity in activities
            ]
        }
        
        return user_data
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None

def create_user(data):
    """
    Create a new user.
    
    Args:
        data (dict): User data containing username, password, phone/email, and role info.
        
    Returns:
        dict: Result of the operation with success status and user ID.
    """
    try:
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        email = data.get('email')
        is_admin = data.get('is_admin', False)
        force_password_change = data.get('force_password_change', False)
        
        # Validation
        if not username or not password:
            return {'success': False, 'error': 'Username and password are required'}
        
        if not phone and not email:
            return {'success': False, 'error': 'Either phone number or email is required'}
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'success': False, 'error': 'Username already exists'}
        
        # Check if phone/email already exists
        if phone:
            existing_phone = User.query.filter_by(phone=phone).first()
            if existing_phone:
                return {'success': False, 'error': 'Phone number already registered'}
        
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                return {'success': False, 'error': 'Email address already registered'}
        
        # Create new user
        new_user = User(
            username=username,
            phone=phone,
            email=email,
            is_admin=is_admin,
            force_password_change=force_password_change
        )
        new_user.password_hash = generate_password_hash(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log system activity
        activity = SystemActivity(
            user_id=new_user.id,
            type='user_created',
            description=f'User account created: {username}',
            timestamp=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return {'success': True, 'user_id': new_user.id, 'message': f'User {username} created successfully'}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {e}")
        return {'success': False, 'error': str(e)}

def update_user(user_id, data):
    """
    Update an existing user.
    
    Args:
        user_id (int): The ID of the user to update.
        data (dict): Updated user data.
        
    Returns:
        dict: Result of the operation.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        # Update basic fields
        user.username = data.get('username', user.username)
        user.phone = data.get('phone', user.phone)
        user.email = data.get('email', user.email)
        user.is_admin = data.get('is_admin', user.is_admin)
        user.force_password_change = data.get('force_password_change', user.force_password_change)
        user.updated_at = datetime.now()
        
        # Update password if provided
        new_password = data.get('password')
        if new_password:
            user.password_hash = generate_password_hash(new_password)
            user.force_password_change = data.get('force_password_change', False)
        
        db.session.commit()
        
        # Log system activity
        activity = SystemActivity(
            user_id=user.id,
            type='user_updated',
            description=f'User account updated: {user.username}',
            timestamp=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return {'success': True, 'message': f'User {user.username} updated successfully'}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user: {e}")
        return {'success': False, 'error': str(e)}

def delete_user(user_id):
    """
    Delete a user (soft delete by deactivating).
    
    Args:
        user_id (int): The ID of the user to delete.
        
    Returns:
        dict: Result of the operation.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        # Don't allow deletion of the last admin user
        if user.is_admin:
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count <= 1:
                return {'success': False, 'error': 'Cannot delete the last admin user'}
        
        username = user.username
        
        # For now, we'll do a hard delete, but in production you might want soft delete
        db.session.delete(user)
        db.session.commit()
        
        # Log system activity (need to use a different user_id since this user is deleted)
        admin_user = User.query.filter_by(is_admin=True).first()
        if admin_user:
            activity = SystemActivity(
                user_id=admin_user.id,
                type='user_deleted',
                description=f'User account deleted: {username}',
                timestamp=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
        
        return {'success': True, 'message': f'User {username} deleted successfully'}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting user: {e}")
        return {'success': False, 'error': str(e)}

def toggle_user_admin_status(user_id):
    """
    Toggle admin status for a user.
    
    Args:
        user_id (int): The ID of the user.
        
    Returns:
        dict: Result of the operation.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        # If removing admin privileges, ensure there's at least one admin left
        if user.is_admin:
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count <= 1:
                return {'success': False, 'error': 'Cannot remove admin privileges from the last admin user'}
        
        # Toggle admin status
        user.is_admin = not user.is_admin
        user.updated_at = datetime.now()
        
        db.session.commit()
        
        # Log system activity
        activity = SystemActivity(
            user_id=user.id,
            type='admin_status_changed',
            description=f'Admin status {"granted to" if user.is_admin else "removed from"} user: {user.username}',
            timestamp=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        status = "granted admin privileges" if user.is_admin else "removed admin privileges"
        return {'success': True, 'message': f'Successfully {status} for {user.username}'}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error toggling admin status: {e}")
        return {'success': False, 'error': str(e)}

def force_password_reset(user_id):
    """
    Force a user to reset their password on next login.
    
    Args:
        user_id (int): The ID of the user.
        
    Returns:
        dict: Result of the operation.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        user.force_password_change = True
        user.updated_at = datetime.now()
        
        db.session.commit()
        
        # Log system activity
        activity = SystemActivity(
            user_id=user.id,
            type='password_reset_forced',
            description=f'Password reset forced for user: {user.username}',
            timestamp=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return {'success': True, 'message': f'Password reset forced for {user.username}'}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error forcing password reset: {e}")
        return {'success': False, 'error': str(e)}

def get_user_statistics():
    """
    Get user statistics for the admin dashboard.
    
    Returns:
        dict: User statistics.
    """
    try:
        total_users = User.query.count()
        admin_users = User.query.filter_by(is_admin=True).count()
        regular_users = total_users - admin_users
        users_needing_password_reset = User.query.filter_by(force_password_change=True).count()
        
        # Recent user registrations (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_registrations = User.query.filter(User.created_at >= thirty_days_ago).count()
        
        return {
            'total_users': total_users,
            'admin_users': admin_users,
            'regular_users': regular_users,
            'users_needing_password_reset': users_needing_password_reset,
            'recent_registrations': recent_registrations
        }
    except Exception as e:
        logger.error(f"Error getting user statistics: {e}")
        return {
            'total_users': 0,
            'admin_users': 0,
            'regular_users': 0,
            'users_needing_password_reset': 0,
            'recent_registrations': 0
        }