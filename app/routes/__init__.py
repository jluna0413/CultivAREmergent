"""
Initialization for the routes package.
This file ensures the routes directory is treated as a Python package
and provides a central point for route registration.
"""

import logging

# Import the real registration functions directly
from .routes import register_routes as real_register_routes


def register_routes(app):
    logging.info("[routes/__init__.py] Calling real_register_routes...")
    real_register_routes(app)
    logging.info("[routes/__init__.py] Route registration complete.")


__all__ = ["register_routes"]
