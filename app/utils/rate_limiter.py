"""
Rate limiter module for Flask-Limiter
STRENGTHENED: Enhanced rate limiting configuration for security hardening
"""

from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Enhanced rate limiter configuration with stricter limits
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        "200 per day",          # Daily global limit
        "50 per hour",          # Hourly global limit  
        "10 per minute",        # Minute global limit
    ],
    storage_uri="memory://",    # In-memory storage for development
    strategy="moving-window"    # More accurate rate limiting
)

# Enhanced rate limits for authentication endpoints
AUTH_RATE_LIMITS = {
    "login": "3 per 5 minutes",      # STRENGTHENED: Was 7, now 3 attempts per 5 minutes
    "register": "2 per minute",      # STRENGTHENED: Was unlimited, now strict
    "password_reset": "2 per hour",  # STRENGTHENED: Was unlimited, now strict
    "api_key": "5 per minute",       # STRENGTHENED: Was unlimited, now strict
}

# Enhanced rate limits for API endpoints  
API_RATE_LIMITS = {
    "plants": "100 per hour",        # STRENGTHENED: Was unlimited, now strict
    "strains": "50 per hour",        # STRENGTHENED: Was unlimited, now strict
    "sensors": "200 per hour",       # STRENGTHENED: Was unlimited, now strict
    "upload": "10 per minute",       # STRENGTHENED: Was unlimited, now strict
}

def get_limiter_for_endpoint(endpoint_type: str) -> str:
    """
    Get appropriate rate limit for endpoint type
    
    Args:
        endpoint_type: Type of endpoint ('auth', 'api', 'upload')
        
    Returns:
        Rate limit string
    """
    if endpoint_type == "auth":
        return AUTH_RATE_LIMITS.get("login", "3 per 5 minutes")
    elif endpoint_type == "upload":
        return API_RATE_LIMITS.get("upload", "5 per minute")
    else:
        return "20 per minute"  # Default for unknown endpoints

# Add security headers and blocking mechanisms
def is_rate_limited(endpoint: str) -> bool:
    """
    Check if endpoint is rate limited
    Returns True if request should be blocked
    """
    # This would integrate with the actual rate limiter
    # For now, placeholder implementation
    return False

def get_remaining_quota(endpoint: str) -> int:
    """
    Get remaining quota for endpoint
    Returns remaining number of requests
    """
    # This would integrate with the actual rate limiter
    # For now, placeholder implementation  
    return 99