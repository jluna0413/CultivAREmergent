"""
Rate limiter module for Flask-Limiter
"""

from flask import request
from flask_limiter import Limiter

# Initialize limiter with default key function (IP address)
limiter = Limiter(key_func=lambda: request.remote_addr if request else "127.0.0.1")