# app/fastapi_app/middleware/security.py

import time
import secrets
import redis # Added
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.types import ASGIApp
from typing import Dict, Tuple

# In-memory store for rate limiting
request_counts: Dict[str, Tuple[int, float]] = {}

# Redis client for rate limiting
# TODO: Configure Redis connection from environment variables
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security headers to all responses.
    This is a partial replacement for Flask-Talisman.
    """
    def __init__(self, app: ASGIApp, is_production: bool = True):
        super().__init__(app)
        self.is_production = is_production

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Generate a nonce for each request
        nonce = secrets.token_hex(16)
        request.state.csp_nonce = nonce

        response = await call_next(request)

        # Default CSP for development
        csp_policy = {
            "default-src": ["'self'"],
            "script-src": ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
            "style-src": ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com"],
            "font-src": ["'self'", "https://fonts.gstatic.com"],
            "img-src": ["'self'", "data:", "https://images.unsplash.com"],
            "connect-src": ["'self'"],
            "object-src": ["'none'"],
            "base-uri": ["'self'"],
            "form-action": ["'self'"],
            "frame-ancestors": ["'none'"],
        }

        if self.is_production:
            # Stricter CSP for production
            csp_policy.update({
                "script-src": ["'self'", "'unsafe-inline'"],
                "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
                "connect-src": ["'self'"],
            })

        # Format the CSP dictionary into a string
        csp_header_value = "; ".join([f"{key} {' '.join(value)}" for key, value in csp_policy.items()])

        headers = {
            "Content-Security-Policy": csp_header_value,
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

        for key, value in headers.items():
            response.headers[key] = value

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware.
    A replacement for Flask-Limiter.
    """
    def __init__(self, app: ASGIApp, limit: int = 100, window: int = 60, use_redis: bool = True):
        super().__init__(app)
        self.limit = limit  # requests
        self.window = window  # seconds
        self.use_redis = use_redis

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Get client IP (support proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"

        if self.use_redis:
            try:
                # Use Redis for rate limiting
                current_time = int(time.time())
                key = f"rate_limit:{client_ip}"
                
                # Use a transaction to ensure atomicity
                pipe = redis_client.pipeline()
                pipe.zremrangebyscore(key, 0, current_time - self.window)
                pipe.zadd(key, {current_time: current_time})
                pipe.zcard(key)
                pipe.expire(key, self.window)
                results = pipe.execute()

                count = results[2]
                
                remaining = max(0, self.limit - count)
                reset_time = self.window

                if count > self.limit:
                    response = JSONResponse(
                        status_code=429,
                        content={
                            "error": "Too Many Requests", 
                            "message": f"Rate limit exceeded. Try again in {reset_time} seconds."
                        }
                    )
                    response.headers["X-RateLimit-Limit"] = str(self.limit)
                    response.headers["X-RateLimit-Remaining"] = "0"
                    response.headers["X-RateLimit-Reset"] = str(reset_time)
                    return response

                response = await call_next(request)
                
                response.headers["X-RateLimit-Limit"] = str(self.limit)
                response.headers["X-RateLimit-Remaining"] = str(remaining)
                response.headers["X-RateLimit-Reset"] = str(reset_time)
                
                return response
            except redis.exceptions.ConnectionError:
                # Fallback to in-memory rate limiting if Redis is not available
                self.use_redis = False

        # Fallback to in-memory rate limiting
        current_time = time.time()
        count, window_start = request_counts.get(client_ip, (0, current_time))

        if current_time - window_start > self.window:
            # New window
            count = 0
            window_start = current_time

        # Calculate headers
        remaining = max(0, self.limit - count - 1)
        reset_time = int(self.window - (current_time - window_start))

        if count >= self.limit:
            response = JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests", 
                    "message": f"Rate limit exceeded. Try again in {reset_time} seconds."
                }
            )
            response.headers["X-RateLimit-Limit"] = str(self.limit)
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["X-RateLimit-Reset"] = str(reset_time)
            return response

        request_counts[client_ip] = (count + 1, window_start)
        response = await call_next(request)
        
        # Add rate limit headers to successful response
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)
        
        return response
