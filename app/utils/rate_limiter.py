"""
Production-grade FastAPI Rate Limiter with Redis persistence
Replaces Flask-Limiter with FastAPI-compatible solution

Features:
- Redis backend for persistence (with in-memory fallback)
- Per-IP and per-user rate limiting
- Different limits for auth endpoints vs general API
- Environment variable configuration
- Production-grade error handling
"""

import os
import logging
from typing import Dict, Optional, Callable, Any
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

# Configure logging
logger = logging.getLogger(__name__)

# Environment configuration
DEFAULT_RATE_LIMIT = os.getenv("DEFAULT_RATE_LIMIT", "100/minute")
AUTH_RATE_LIMIT = os.getenv("AUTH_RATE_LIMIT", "10/minute") 
WRITE_RATE_LIMIT = os.getenv("WRITE_RATE_LIMIT", "20/minute")
RATE_LIMIT_STORAGE_URL = os.getenv("RATE_LIMIT_STORAGE_URL")
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"


class FastAPIRateLimiter:
    """
    Production-grade FastAPI rate limiter with Redis persistence
    """
    
    def __init__(self):
        self.limiter = None
        self._initialize_limiter()
    
    def _initialize_limiter(self):
        """Initialize the rate limiter with Redis backend or in-memory fallback"""
        try:
            if RATE_LIMIT_STORAGE_URL:
                # Use Redis backend for production persistence
                self.limiter = Limiter(
                    key_func=get_remote_address,
                    storage_uri=RATE_LIMIT_STORAGE_URL,
                    default_limits=[DEFAULT_RATE_LIMIT]
                )
                logger.info(f"Rate limiter initialized with Redis backend: {RATE_LIMIT_STORAGE_URL}")
            else:
                # In-memory fallback for development
                self.limiter = Limiter(
                    key_func=get_remote_address,
                    default_limits=[DEFAULT_RATE_LIMIT]
                )
                logger.warning("Rate limiter initialized with in-memory backend (development mode)")
        except Exception as e:
            logger.error(f"Failed to initialize rate limiter: {e}")
            # Fallback to in-memory even if Redis fails
            self.limiter = Limiter(
                key_func=get_remote_address,
                default_limits=[DEFAULT_RATE_LIMIT]
            )
            logger.warning("Rate limiter initialized with fallback in-memory backend")
    
    def get_limiter(self) -> Limiter:
        """Get the initialized limiter instance"""
        if not RATE_LIMIT_ENABLED:
            # Return a mock limiter that doesn't enforce limits
            return self._get_mock_limiter()
        return self.limiter
    
    def _get_mock_limiter(self) -> Limiter:
        """Return a mock limiter that doesn't enforce limits when disabled"""
        class MockLimiter:
            def limit(self, *args, **kwargs):
                def decorator(func):
                    return func
                return decorator
        return MockLimiter()


class UserKeyLimiter:
    """
    Rate limiter that uses user identity instead of IP address
    Useful for authenticated endpoints where per-user limits are more appropriate
    """
    
    def __init__(self, limiter: Limiter):
        self.limiter = limiter
    
    def limit_by_user(self, limit: str):
        """Decorator to limit by user ID instead of IP"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # Get user from request context or arguments
                request = None
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
                
                if not request:
                    return await func(*args, **kwargs)
                
                # Try to get user ID from request state or dependencies
                user_id = getattr(request.state, 'user_id', None)
                if not user_id:
                    # Fallback to IP if no user context
                    user_id = get_remote_address(request)
                
                # Apply rate limit based on user ID
                return await self.limiter.limit(f"{user_id}:{limit}")(func)(*args, **kwargs)
            
            return wrapper
        return decorator


class RateLimitConfig:
    """
    Configuration class for different rate limiting strategies
    """
    
    # Standard limits
    GENERAL_API = DEFAULT_RATE_LIMIT
    AUTH_ENDPOINTS = AUTH_RATE_LIMIT  
    WRITE_OPERATIONS = WRITE_RATE_LIMIT
    SENSITIVE_ENDPOINTS = "5/minute"
    
    # Per-user limits (more restrictive)
    USER_API = "50/hour"
    USER_WRITE = "10/hour"
    ADMIN_ENDPOINTS = "1000/hour"
    
    @classmethod
    def get_limit_for_endpoint(cls, endpoint_type: str) -> str:
        """Get appropriate rate limit for endpoint type"""
        limits = {
            'auth': cls.AUTH_ENDPOINTS,
            'write': cls.WRITE_OPERATIONS,
            'admin': cls.ADMIN_ENDPOINTS,
            'sensitive': cls.SENSITIVE_ENDPOINTS,
            'user': cls.USER_API,
            'general': cls.GENERAL_API
        }
        return limits.get(endpoint_type, cls.GENERAL_API)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware for additional rate limiting logic
    Handles edge cases and special requirements
    """
    
    def __init__(self, app, limiter: Limiter):
        super().__init__(app)
        self.limiter = limiter
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for certain paths
        if self._should_skip_rate_limit(request):
            return await call_next(request)
        
        # Apply additional custom logic if needed
        try:
            response = await call_next(request)
            return response
        except RateLimitExceeded as e:
            logger.warning(f"Rate limit exceeded for {get_remote_address(request)}: {e}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please slow down your requests.",
                headers={"Retry-After": str(int(e.retry_after))} if e.retry_after else None
            )
    
    def _should_skip_rate_limit(self, request: Request) -> bool:
        """Check if rate limiting should be skipped for this request"""
        skip_paths = [
            "/health",
            "/ping", 
            "/api/v1/system/info",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]
        
        return any(request.url.path.startswith(path) for path in skip_paths)


# Global rate limiter instance
rate_limiter = FastAPIRateLimiter()

# Backward compatibility for Flask blueprints
limiter = rate_limiter.get_limiter()


def get_rate_limiter() -> Limiter:
    """Dependency to get the rate limiter instance"""
    return rate_limiter.get_limiter()


def create_user_limiter(limiter: Limiter) -> UserKeyLimiter:
    """Factory function to create user-based rate limiter"""
    return UserKeyLimiter(limiter)


# Export rate limiting decorators for easy use
def rate_limit(limit: str):
    """Decorator for rate limiting endpoints"""
    limiter = rate_limiter.get_limiter()
    return limiter.limit(limit)


def rate_limit_by_user(limit: str):
    """Decorator for rate limiting by user ID instead of IP"""
    limiter = rate_limiter.get_limiter()
    user_limiter = UserKeyLimiter(limiter)
    return user_limiter.limit_by_user(limit)


def rate_limit_by_endpoint(endpoint_type: str):
    """Decorator for rate limiting with predefined limits by endpoint type"""
    limit = RateLimitConfig.get_limit_for_endpoint(endpoint_type)
    return rate_limit(limit)


# Production configuration example:
"""
Environment Variables:
- RATE_LIMIT_ENABLED=true/false (default: true)
- RATE_LIMIT_STORAGE_URL=redis://localhost:6379/0 (optional)
- DEFAULT_RATE_LIMIT=100/minute (default)
- AUTH_RATE_LIMIT=10/minute (default)  
- WRITE_RATE_LIMIT=20/minute (default)

Usage Examples:
1. Basic rate limiting: @rate_limit("50/minute")
2. By endpoint type: @rate_limit_by_endpoint("auth")  
3. By user: @rate_limit_by_user("100/hour")
4. In dependencies: limiter = Depends(get_rate_limiter)
"""