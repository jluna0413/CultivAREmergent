"""
Enhanced Security Middleware for Flask Application
Provides comprehensive security headers and input validation
"""

import re
import html
import urllib.parse
from flask import request, g, session
from functools import wraps
import secrets
import string
from datetime import timedelta


class SecurityMiddleware:
    """Comprehensive security middleware for Flask applications"""
    
    # Secure charset pattern - only allow safe characters
    SAFE_CHARSET_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
    
    # Event handler blacklist patterns
    EVENT_HANDLER_BLACKLIST = [
        r'on\\w+\\s*=',  # onload, onclick, etc.
        r'javascript:',  # javascript: protocol
        r'<script',  # script tags
        r'data:',  # data: protocol
        r'vbscript:',  # vbscript protocol
        r'document\\.cookie',  # cookie access
        r'eval\\(',  # eval functions
        r'innerHTML',  # innerHTML manipulation
        r'outerHTML',  # outerHTML manipulation
        r'insertAdjacentHTML',  # HTML insertion
    ]
    
    @staticmethod
    def sanitize_input(input_string, max_length=1000):
        """
        Sanitize user input to prevent XSS and injection attacks
        
        Args:
            input_string (str): Raw user input
            max_length (int): Maximum allowed length
            
        Returns:
            str: Sanitized input
        """
        if not isinstance(input_string, str):
            return ""
        
        # Limit length
        input_string = input_string[:max_length]
        
        # Remove potentially dangerous characters - FIXED REGEX
        input_string = re.sub(r"[<>'\"]", "", input_string)
        
        # Encode HTML entities
        input_string = html.escape(input_string)
        
        # Remove null bytes
        input_string = input_string.replace('\\x00', '')
        
        return input_string.strip()
    
    @staticmethod
    def validate_charset(charset_value):
        """
        Validate charset parameter to prevent injection
        
        Args:
            charset_value (str): Charset value to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not charset_value:
            return True  # Empty is allowed
        
        # Only allow alphanumeric, dash, underscore
        if not re.match(r'^[a-zA-Z0-9._-]+$', charset_value):
            return False
        
        # Limit length
        if len(charset_value) > 50:
            return False
        
        return True
    
    @staticmethod
    def check_event_handlers(html_content):
        """
        Check for user controllable event handlers in HTML
        
        Args:
            html_content (str): HTML content to check
            
        Returns:
            dict: Security report with violations
        """
        violations = []
        
        for pattern in SecurityMiddleware.EVENT_HANDLER_BLACKLIST:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                violations.extend(matches)
        
        return {
            'has_violations': len(violations) > 0,
            'violations': violations,
            'total_violations': len(violations)
        }
    
    @staticmethod
    def generate_secure_token(length=32):
        """Generate cryptographically secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def set_secure_cookie(app, session, cookie_name, cookie_value, max_age=86400):
        """
        Set cookie with comprehensive security attributes
        
        Args:
            app: Flask app instance
            session: Session object
            cookie_name (str): Name of the cookie
            cookie_value (str): Value of the cookie
            max_age (int): Maximum age in seconds (24 hours default)
        """
        session[cookie_name] = cookie_value
        
        # Set secure cookie attributes
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=max_age)


def sanitize_route_inputs(f):
    """
    Decorator to sanitize all route inputs
    Apply this to Flask routes that accept user input
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Sanitize query parameters
        sanitized_args = {}
        for key, value in request.args.items():
            sanitized_args[key] = SecurityMiddleware.sanitize_input(value)
        
        # Sanitize form data
        sanitized_form = {}
        for key, value in request.form.items():
            sanitized_form[key] = SecurityMiddleware.sanitize_input(value)
        
        # Store sanitized data in g object for route access
        g.sanitized_args = sanitized_args
        g.sanitized_form = sanitized_form
        
        # Validate charset
        charset = request.headers.get('Content-Type', '')
        if 'charset=' in charset:
            charset_value = charset.split('charset=')[1].split(';')[0].strip()
            if not SecurityMiddleware.validate_charset(charset_value):
                return "Invalid character encoding", 400
        
        return f(*args, **kwargs)
    
    return decorated_function


def add_security_headers(app):
    """
    Add comprehensive security headers to Flask application
    
    Args:
        app: Flask app instance
    """
    
    @app.after_request
    def add_security_headers(response):
        # Cache-Control headers for security
        if request.endpoint and request.method in ['GET', 'POST', 'PUT', 'DELETE']:
            # No-cache for sensitive endpoints
            if any(endpoint in request.endpoint for endpoint in ['auth', 'admin', 'dashboard', 'api']):
                response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
            else:
                # Cache for static content only
                response.headers['Cache-Control'] = 'public, max-age=3600'
        
        # Content-Type protection
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # XSS Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Frame protection
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-src 'none'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers['Content-Security-Policy'] = csp
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response.headers['Permissions-Policy'] = (
            'geolocation=(), '
            'camera=(), '
            'microphone=(), '
            'payment=(), '
            'usb=()'
        )
        
        # Additional security headers
        response.headers['X-Permitted-Cross-Domain-Policies'] = 'none'
        response.headers['X-Download-Options'] = 'noopen'
        
        return response


def implement_csrf_protection(app):
    """
    Enhanced CSRF protection implementation
    
    Args:
        app: Flask app instance
    """
    try:
        from flask_wtf.csrf import CSRFProtect, generate_csrf
        from flask import g
        
        # Initialize CSRF protection
        csrf = CSRFProtect(app)
        app.config['WTF_CSRF_TIME_LIMIT'] = None
        
        @app.context_processor
        def inject_csrf_token():
            return dict(csrf_token=generate_csrf)
        
        @app.before_request
        def check_csrf_token():
            """Check CSRF token for all state-changing requests"""
            if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                # Skip CSRF for API endpoints that use their own auth
                if request.endpoint and not any(
                    skip_endpoint in request.endpoint 
                    for skip_endpoint in ['api.', 'auth.']
                ):
                    # Force CSRF validation
                    csrf.protect()
    except ImportError:
        print("WARNING: Flask-WTF not available, CSRF protection disabled")


def validate_html_safety(template_content, template_path=""):
    """
    Validate HTML templates for security issues
    
    Args:
        template_content (str): Template content to validate
        template_path (str): Path for reporting purposes
        
    Returns:
        dict: Security validation results
    """
    validation_results = {
        'template_path': template_path,
        'is_safe': True,
        'violations': [],
        'warnings': []
    }
    
    # Check for event handlers
    event_handler_report = SecurityMiddleware.check_event_handlers(template_content)
    if event_handler_report['has_violations']:
        validation_results['violations'].append({
            'type': 'Event Handlers',
            'details': event_handler_report['violations'],
            'severity': 'HIGH'
        })
        validation_results['is_safe'] = False
    
    # Check for unsafe Jinja2 usage
    if '{{' in template_content and '|' not in template_content:
        validation_results['warnings'].append({
            'type': 'Unescaped Output',
            'message': 'Found {{ }} without proper escaping',
            'severity': 'MEDIUM'
        })
    
    # Check for script tags
    script_pattern = re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)
    if script_pattern.search(template_content):
        validation_results['warnings'].append({
            'type': 'Inline Scripts',
            'message': 'Found script tags that may need review',
            'severity': 'MEDIUM'
        })
    
    return validation_results