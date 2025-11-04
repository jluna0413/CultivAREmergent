"""
Structured request logging middleware for FastAPI application
Provides observability, request tracing, and performance monitoring
"""

import time
import uuid
import json
import logging
from typing import Callable, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response as FastAPIResponse

from app.fastapi_app.routers.health import metrics

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured request logging with request IDs and observability
    """
    
    def __init__(self, app, include_request_body: bool = False, max_body_size: int = 10240):
        super().__init__(app)
        self.include_request_body = include_request_body
        self.max_body_size = max_body_size
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Start timing
        start_time = time.time()
        
        # Extract request information
        request_info = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
            "timestamp": time.time()
        }
        
        # Add request body for POST/PUT/PATCH requests (limited)
        if self.include_request_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                # Read request body (limited size)
                body = await request.body()
                if len(body) <= self.max_body_size:
                    try:
                        # Try to parse as JSON
                        body_str = body.decode('utf-8')
                        request_info["body"] = json.loads(body_str) if body_str.strip().startswith(('{', '[')) else {"raw": body_str}
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        request_info["body"] = {"raw": "[binary data]"}
                else:
                    request_info["body"] = {"error": f"Body too large: {len(body)} bytes"}
            except Exception as e:
                request_info["body"] = {"error": f"Failed to read body: {str(e)}"}
        
        # Store request ID in request state for use in handlers
        request.state.request_id = request_id
        
        # Log request start
        logger.info(f"Request started: {request_id} {request.method} {request.url.path}")
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Extract response information
            response_info = {
                "request_id": request_id,
                "status_code": response.status_code,
                "response_time": response_time,
                "response_size": self._get_response_size(response),
                "timestamp": time.time()
            }
            
            # Record metrics
            endpoint = self._normalize_endpoint(request.url.path)
            metrics.record_request(
                method=request.method,
                endpoint=endpoint,
                status_code=response.status_code,
                response_time=response_time
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{response_time:.4f}"
            
            # Log response
            log_level = self._get_log_level(response.status_code)
            log_message = f"Request completed: {request_id} {request.method} {request.url.path} - {response.status_code} ({response_time:.4f}s)"
            
            if log_level == "error":
                logger.error(log_message)
            elif log_level == "warning":
                logger.warning(log_message)
            else:
                logger.info(log_message)
            
            # Log structured data if debug level
            if logger.isEnabledFor(logging.DEBUG):
                debug_info = {
                    "request": request_info,
                    "response": response_info
                }
                logger.debug(f"Request details: {json.dumps(debug_info, indent=2)}")
            
            return response
            
        except Exception as e:
            # Calculate response time for failed requests
            response_time = time.time() - start_time
            
            # Record error metrics
            endpoint = self._normalize_endpoint(request.url.path)
            metrics.record_request(
                method=request.method,
                endpoint=endpoint,
                status_code=500,
                response_time=response_time
            )
            
            # Log error with full context
            error_info = {
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "error": str(e),
                "error_type": type(e).__name__,
                "response_time": response_time
            }
            logger.error(f"Request failed: {request_id} {request.method} {request.url.path} - {str(e)}", extra=error_info)
            
            # Re-raise exception
            raise
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct client IP
        if hasattr(request.client, "host") and request.client.host:
            return request.client.host
        
        return "unknown"
    
    def _get_response_size(self, response: Response) -> int:
        """Get response size in bytes"""
        if hasattr(response, "body"):
            return len(response.body) if response.body else 0
        return 0
    
    def _normalize_endpoint(self, path: str) -> str:
        """Normalize endpoint path for metrics aggregation"""
        # Remove dynamic segments like UUIDs, IDs, etc.
        import re
        
        # Replace UUID patterns
        path = re.sub(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '/{uuid}', path)
        
        # Replace numeric IDs
        path = re.sub(r'/\d+', '/{id}', path)
        
        # Replace UUID-like strings
        path = re.sub(r'/[0-9a-f]{32}', '/{hash}', path)
        
        return path
    
    def _get_log_level(self, status_code: int) -> str:
        """Determine log level based on status code"""
        if status_code >= 500:
            return "error"
        elif status_code >= 400:
            return "warning"
        else:
            return "info"


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Additional middleware for performance monitoring and alerting
    """
    
    def __init__(self, app, slow_request_threshold: float = 2.0):
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
        self.request_counts = {}
        self.slow_requests = []
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            response_time = time.time() - start_time
            
            # Track slow requests
            if response_time > self.slow_request_threshold:
                slow_request_info = {
                    "timestamp": time.time(),
                    "request_id": getattr(request.state, 'request_id', 'unknown'),
                    "method": request.method,
                    "path": request.url.path,
                    "response_time": response_time,
                    "status_code": response.status_code
                }
                self.slow_requests.append(slow_request_info)
                
                # Keep only recent slow requests (last 100)
                if len(self.slow_requests) > 100:
                    self.slow_requests = self.slow_requests[-100:]
                
                # Log slow request
                logger.warning(f"Slow request detected: {request.method} {request.url.path} took {response_time:.4f}s")
            
            # Track request frequency per endpoint
            endpoint = self._normalize_endpoint(request.url.path)
            if endpoint not in self.request_counts:
                self.request_counts[endpoint] = 0
            self.request_counts[endpoint] += 1
            
            return response
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Request failed after {response_time:.4f}s: {str(e)}")
            raise
    
    def _normalize_endpoint(self, path: str) -> str:
        """Normalize endpoint path for metrics aggregation"""
        import re
        
        # Replace UUID patterns
        path = re.sub(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '/{uuid}', path)
        
        # Replace numeric IDs
        path = re.sub(r'/\d+', '/{id}', path)
        
        # Replace UUID-like strings
        path = re.sub(r'/[0-9a-f]{32}', '/{hash}', path)
        
        return path
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance monitoring summary"""
        return {
            "slow_requests": len(self.slow_requests),
            "slow_request_threshold": self.slow_request_threshold,
            "recent_slow_requests": self.slow_requests[-10:],  # Last 10 slow requests
            "request_counts": dict(sorted(self.request_counts.items(), key=lambda x: x[1], reverse=True))
        }


class SecurityMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Middleware for security monitoring and threat detection
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.suspicious_patterns = [
            r'(\.\./|\.\.\\)',  # Path traversal
            r'(<script|javascript:|vbscript:)',  # XSS
            r'(union.*select|drop\s+table|insert\s+into)',  # SQL injection
            r'(\?.*\&.*\=.*\&)',  # Parameter pollution
            r'(\%3C\%3E|\%3C|\%3E)',  # Encoded script tags
        ]
        self.suspicious_requests = []
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check for suspicious patterns
        is_suspicious = False
        suspicious_reasons = []
        
        url = str(request.url)
        headers = dict(request.headers)
        
        # Check URL for suspicious patterns
        import re
        for pattern in self.suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                is_suspicious = True
                suspicious_reasons.append(f"URL pattern: {pattern}")
        
        # Check headers for suspicious content
        for header_name, header_value in headers.items():
            if header_value and re.search(r'(<script|javascript:|data:.*base64)', header_value, re.IGNORECASE):
                is_suspicious = True
                suspicious_reasons.append(f"Suspicious header: {header_name}")
        
        # Log suspicious requests
        if is_suspicious:
            suspicious_info = {
                "timestamp": time.time(),
                "request_id": getattr(request.state, 'request_id', 'unknown'),
                "client_ip": self._get_client_ip(request),
                "method": request.method,
                "url": url,
                "user_agent": headers.get("user-agent", ""),
                "reasons": suspicious_reasons
            }
            self.suspicious_requests.append(suspicious_info)
            
            # Keep only recent suspicious requests (last 50)
            if len(self.suspicious_requests) > 50:
                self.suspicious_requests = self.suspicious_requests[-50:]
            
            logger.warning(f"Suspicious request detected: {suspicious_info['client_ip']} {request.method} {url}")
        
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Request processing failed: {str(e)}")
            raise
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        if hasattr(request.client, "host") and request.client.host:
            return request.client.host
        
        return "unknown"
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security monitoring summary"""
        return {
            "suspicious_requests": len(self.suspicious_requests),
            "recent_suspicious_requests": self.suspicious_requests[-10:],  # Last 10 suspicious requests
            "monitoring_patterns": len(self.suspicious_patterns)
        }