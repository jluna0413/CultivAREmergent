"""
Initialization for the routes package.
This file ensures the routes directory is treated as a Python package
and provides a central point for route registration.
"""



# Import the real registration functions directly
from .routes import register_routes as real_register_routes
from .admin_api import register_admin_api_routes as real_register_admin_api_routes

import logging
def register_routes(app):
    logging.info("[routes/__init__.py] Calling real_register_routes...")
    real_register_routes(app)
    logging.info("[routes/__init__.py] Calling real_register_admin_api_routes...")
    real_register_admin_api_routes(app)
    logging.info("[routes/__init__.py] Route registration complete.")

def register_admin_api_routes(app):
    logging.info("[routes/__init__.py] Calling real_register_admin_api_routes (direct)...")
    real_register_admin_api_routes(app)
    logging.info("[routes/__init__.py] Admin API route registration complete.")

__all__ = ['register_routes', 'register_admin_api_routes']
