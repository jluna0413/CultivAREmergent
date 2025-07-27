"""
Data export routes for the CultivAR application.
"""

from flask import render_template, request, jsonify, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from app.handlers.export_handlers import (
    export_plants_csv, export_strains_csv, export_activities_csv, export_users_csv,
    export_plants_json, export_strains_json, export_complete_backup, export_sensors_csv,
    get_export_statistics
)
from app.models.system_models import SystemActivity
from app.models import db
from io import BytesIO

def register_export_routes(app):
    """
    Register data export routes.
    
    Args:
        app: The Flask application.
    """
    
    @app.route('/admin/export')
    @login_required
    def admin_export():
        """Admin page for data export."""
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('protected_dashboard'))
        
        export_stats = get_export_statistics()
        
        return render_template('admin/export.html', 
                               title='Data Export & Backup',
                               export_stats=export_stats)
    
    @app.route('/admin/export/plants/<format>')
    @login_required
    def export_plants(format):
        """Export plants data."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if format.lower() == 'csv':
                data = export_plants_csv()
                if data:
                    # Log the export activity
                    activity = SystemActivity(
                        user_id=current_user.id,
                        type='data_export',
                        description='Plants data exported to CSV',
                        timestamp=datetime.now()
                    )
                    db.session.add(activity)
                    db.session.commit()
                    
                    return send_file(
                        BytesIO(data.encode('utf-8')),
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'cultivar_plants_{timestamp}.csv'
                    )
            
            elif format.lower() == 'json':
                data = export_plants_json()
                if data:
                    # Log the export activity
                    activity = SystemActivity(
                        user_id=current_user.id,
                        type='data_export',
                        description='Plants data exported to JSON',
                        timestamp=datetime.now()
                    )
                    db.session.add(activity)
                    db.session.commit()
                    
                    return send_file(
                        BytesIO(data.encode('utf-8')),
                        mimetype='application/json',
                        as_attachment=True,
                        download_name=f'cultivar_plants_{timestamp}.json'
                    )
            
            return jsonify({'success': False, 'error': 'Invalid format or export failed'})
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/admin/export/strains/<format>')
    @login_required
    def export_strains(format):
        """Export strains data."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if format.lower() == 'csv':
                data = export_strains_csv()
                if data:
                    # Log the export activity
                    activity = SystemActivity(
                        user_id=current_user.id,
                        type='data_export',
                        description='Strains data exported to CSV',
                        timestamp=datetime.now()
                    )
                    db.session.add(activity)
                    db.session.commit()
                    
                    return send_file(
                        BytesIO(data.encode('utf-8')),
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'cultivar_strains_{timestamp}.csv'
                    )
            
            elif format.lower() == 'json':
                data = export_strains_json()
                if data:
                    # Log the export activity
                    activity = SystemActivity(
                        user_id=current_user.id,
                        type='data_export',
                        description='Strains data exported to JSON',
                        timestamp=datetime.now()
                    )
                    db.session.add(activity)
                    db.session.commit()
                    
                    return send_file(
                        BytesIO(data.encode('utf-8')),
                        mimetype='application/json',
                        as_attachment=True,
                        download_name=f'cultivar_strains_{timestamp}.json'
                    )
            
            return jsonify({'success': False, 'error': 'Invalid format or export failed'})
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/admin/export/activities')
    @login_required
    def export_activities():
        """Export activities data."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            data = export_activities_csv()
            
            if data:
                # Log the export activity
                activity = SystemActivity(
                    user_id=current_user.id,
                    type='data_export',
                    description='Activities data exported to CSV',
                    timestamp=datetime.now()
                )
                db.session.add(activity)
                db.session.commit()
                
                return send_file(
                    BytesIO(data.encode('utf-8')),
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'cultivar_activities_{timestamp}.csv'
                )
            
            return jsonify({'success': False, 'error': 'Export failed'})
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/admin/export/users')
    @login_required
    def export_users():
        """Export users data."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            data = export_users_csv()
            
            if data:
                # Log the export activity
                activity = SystemActivity(
                    user_id=current_user.id,
                    type='data_export',
                    description='Users data exported to CSV',
                    timestamp=datetime.now()
                )
                db.session.add(activity)
                db.session.commit()
                
                return send_file(
                    BytesIO(data.encode('utf-8')),
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'cultivar_users_{timestamp}.csv'
                )
            
            return jsonify({'success': False, 'error': 'Export failed'})
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/admin/export/sensors')
    @login_required
    def export_sensors():
        """Export sensors data."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            data = export_sensors_csv()
            
            if data:
                # Log the export activity
                activity = SystemActivity(
                    user_id=current_user.id,
                    type='data_export',
                    description='Sensors data exported to CSV',
                    timestamp=datetime.now()
                )
                db.session.add(activity)
                db.session.commit()
                
                return send_file(
                    BytesIO(data.encode('utf-8')),
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'cultivar_sensors_{timestamp}.csv'
                )
            
            return jsonify({'success': False, 'error': 'Export failed'})
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/admin/export/complete')
    @login_required
    def export_complete():
        """Create complete system backup."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_data = export_complete_backup()
            
            if backup_data:
                # Log the export activity
                activity = SystemActivity(
                    user_id=current_user.id,
                    type='data_export',
                    description='Complete system backup created',
                    timestamp=datetime.now()
                )
                db.session.add(activity)
                db.session.commit()
                
                return send_file(
                    backup_data,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name=f'cultivar_complete_backup_{timestamp}.zip'
                )
            
            return jsonify({'success': False, 'error': 'Backup creation failed'})
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    # API endpoints for export statistics
    @app.route('/api/admin/export/stats')
    @login_required
    def api_export_stats():
        """API endpoint to get export statistics."""
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Access denied'})
        
        stats = get_export_statistics()
        return jsonify({'success': True, 'stats': stats})