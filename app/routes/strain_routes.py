"""
Strain routes for the CultivAR application.
"""

from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required
from app.handlers import strain_handlers, breeder_handlers
from app.config import Config
from app.config.load_config import load_config_from_db

def register_strain_routes(app):
    """
    Register strain routes.

    Args:
        app: The Flask application.
    """
    @app.route('/strains/add')
    @login_required
    def add_strain_page():
        """Render the add strain page."""
        return render_template('views/add_strain.html',
                              title='Add New Strain',
                              breeders=Config.Breeders)

    @app.route('/breeders/add')
    @login_required
    def add_breeder():
        """Render the add breeder page."""
        return render_template('views/add_breeder.html',
                              title='Add New Breeder')
