"""
User management routes for the CultivAR application.
"""

from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.handlers.user_handlers import (
    get_all_users, get_user_by_id, create_user, update_user, delete_user,
    toggle_user_admin_status, force_password_reset, get_user_statistics
)

def register_user_management_routes(app):
    """
    Register user management routes.
    
    Args:
        app: The Flask application.
    """
    
    @app.route('/admin/users')
    @login_required
    def admin_users():
        """Admin page for user management."""
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('protected_dashboard'))
        
        users = get_all_users()
        user_stats = get_user_statistics()
        
        return render_template('admin/users.html', 
                               title='User Management',
                               users=users,
                               user_stats=user_stats)
    
    @app.route('/admin/users/create', methods=['GET', 'POST'])
    @login_required
    def admin_create_user():
        """Create a new user."""
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('protected_dashboard'))
        
        if request.method == 'POST':
            user_data = {
                'username': request.form.get('username'),
                'password': request.form.get('password'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'is_admin': request.form.get('is_admin') == 'on',
                'force_password_change': request.form.get('force_password_change') == 'on'
            }
            
            result = create_user(user_data)
            
            if result['success']:
                flash(result['message'], 'success')
                return redirect(url_for('admin_users'))
            else:
                flash(result['error'], 'danger')
        
        return render_template('admin/create_user.html', title='Create User')
    
    @app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
    @login_required
    def admin_edit_user(user_id):
        """Edit an existing user."""
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('protected_dashboard'))
        
        user = get_user_by_id(user_id)
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('admin_users'))
        
        if request.method == 'POST':
            user_data = {
                'username': request.form.get('username'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'is_admin': request.form.get('is_admin') == 'on',
                'force_password_change': request.form.get('force_password_change') == 'on'
            }
            
            # Only update password if provided
            password = request.form.get('password')
            if password:
                user_data['password'] = password
            
            result = update_user(user_id, user_data)
            
            if result['success']:
                flash(result['message'], 'success')
                return redirect(url_for('admin_users'))
            else:
                flash(result['error'], 'danger')
        
        return render_template('admin/edit_user.html', title='Edit User', user=user)
    
    @app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
    @login_required
    def admin_delete_user(user_id):
        """Delete a user."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        result = delete_user(user_id)
        return jsonify(result)
    
    @app.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
    @login_required
    def admin_toggle_user_admin(user_id):
        """Toggle admin status for a user."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        result = toggle_user_admin_status(user_id)
        return jsonify(result)
    
    @app.route('/admin/users/<int:user_id>/force-password-reset', methods=['POST'])
    @login_required
    def admin_force_password_reset(user_id):
        """Force password reset for a user."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        result = force_password_reset(user_id)
        return jsonify(result)
    
    # API endpoints for AJAX requests
    @app.route('/api/admin/users')
    @login_required
    def api_get_users():
        """API endpoint to get all users."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        users = get_all_users()
        return jsonify({'success': True, 'users': users})
    
    @app.route('/api/admin/users/<int:user_id>')
    @login_required
    def api_get_user(user_id):
        """API endpoint to get a specific user."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        user = get_user_by_id(user_id)
        if user:
            return jsonify({'success': True, 'user': user})
        else:
            return jsonify({'success': False, 'error': 'User not found'})
    
    @app.route('/api/admin/users/stats')
    @login_required
    def api_get_user_stats():
        """API endpoint to get user statistics."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        stats = get_user_statistics()
        return jsonify({'success': True, 'stats': stats})