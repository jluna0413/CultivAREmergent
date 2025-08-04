"""
Clone management routes for the CultivAR application.
"""

from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.handlers.clone_handlers import (
    get_available_parent_plants, create_clones, get_clone_lineage, get_clone_statistics,
    get_all_clones, delete_clone
)
from app.models.base_models import Zone

def register_clone_routes(app):
    """
    Register clone management routes.
    
    Args:
        app: The Flask application.
    """
    
    @app.route('/clones')
    @login_required
    def clones_dashboard():
        """Clone management dashboard."""
        clone_stats = get_clone_statistics()
        all_clones = get_all_clones()
        
        return render_template('clones/dashboard.html',
                               title='Clone Management',
                               clone_stats=clone_stats,
                               clones=all_clones)
    
    @app.route('/clones/create', methods=['GET', 'POST'])
    @login_required
    def create_clone():
        """Create new clones from a parent plant."""
        if request.method == 'POST':
            parent_id = request.form.get('parent_id')
            clone_count = int(request.form.get('clone_count', 1))
            
            if not parent_id:
                flash('Please select a parent plant.', 'danger')
                return redirect(url_for('create_clone'))
            
            # Build clone data list
            clone_data_list = []
            for i in range(clone_count):
                clone_name = request.form.get(f'clone_name_{i}', f'Clone {i+1}')
                clone_description = request.form.get(f'clone_description_{i}', '')
                zone_id = request.form.get(f'zone_id_{i}')
                start_date = request.form.get(f'start_date_{i}')
                
                clone_data = {
                    'name': clone_name,
                    'description': clone_description,
                    'zone_id': int(zone_id) if zone_id else None,
                    'start_date': start_date
                }
                clone_data_list.append(clone_data)
            
            # Create the clones
            result = create_clones(parent_id, clone_data_list, current_user.id)
            
            if result['success']:
                flash(result['message'], 'success')
                if 'errors' in result and result['errors']:
                    for error in result['errors']:
                        flash(f'Warning: {error}', 'warning')
                return redirect(url_for('clones_dashboard'))
            else:
                flash(result['error'], 'danger')
                if 'errors' in result and result['errors']:
                    for error in result['errors']:
                        flash(f'Error: {error}', 'danger')
        
        # GET request - show the form
        parent_plants = get_available_parent_plants()
        zones = Zone.query.all()
        
        return render_template('clones/create.html',
                               title='Create Clones',
                               parent_plants=parent_plants,
                               zones=zones)
    
    @app.route('/clones/<int:clone_id>/lineage')
    @login_required
    def clone_lineage(clone_id):
        """View clone lineage (family tree)."""
        lineage_result = get_clone_lineage(clone_id)
        
        if not lineage_result['success']:
            flash(lineage_result['error'], 'danger')
            return redirect(url_for('clones_dashboard'))
        
        return render_template('clones/lineage.html',
                               title='Clone Lineage',
                               lineage=lineage_result['lineage'])
    
    @app.route('/clones/<int:clone_id>/delete', methods=['POST'])
    @login_required
    def delete_clone_route(clone_id):
        """Delete a clone."""
        result = delete_clone(clone_id, current_user.id)
        return jsonify(result)
    
    # API endpoints
    @app.route('/api/clones/stats')
    @login_required
    def api_clone_stats():
        """API endpoint to get clone statistics."""
        stats = get_clone_statistics()
        return jsonify({'success': True, 'stats': stats})
    
    @app.route('/api/clones/parents')
    @login_required
    def api_available_parents():
        """API endpoint to get available parent plants."""
        parents = get_available_parent_plants()
        return jsonify({'success': True, 'parents': parents})
    
    @app.route('/api/clones')
    @login_required
    def api_all_clones():
        """API endpoint to get all clones."""
        clones = get_all_clones()
        return jsonify({'success': True, 'clones': clones})
    
    @app.route('/api/clones/<int:clone_id>/lineage')
    @login_required
    def api_clone_lineage(clone_id):
        """API endpoint to get clone lineage."""
        lineage_result = get_clone_lineage(clone_id)
        return jsonify(lineage_result)