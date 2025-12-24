"""
Centralized Input Validation Middleware for CultivAR
UNIFIED: Consistent validation across Flask and FastAPI implementations
STRENGTHENED: Enhanced XSS protection and input sanitization
"""

import re
import html
import bleach
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class SecurityValidationError(Exception):
    """Raised when security validation fails"""
    pass


class InputValidationMiddleware:
    """
    Unified input validation middleware for both Flask and FastAPI
    Provides consistent XSS protection and input sanitization
    """
    
    # Enhanced dangerous patterns for XSS detection
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',           # Script tags
        r'javascript:',                         # JavaScript protocol
        r'on\w+\s*=',                          # Event handlers (onclick, onload, etc.)
        r'vbscript:',                          # VBScript protocol
        r'data:text/html',                     # Data URI
        r'eval\s*\(',                          # Eval functions
        r'expression\s*\(',                    # CSS expressions
        r'url\s*\(\s*javascript:',             # URL javascript
        r'<iframe[^>]*>.*?</iframe>',          # Iframe elements
        r'<object[^>]*>.*?</object>',          # Object elements
        r'<embed[^>]*>.*?</embed>',            # Embed elements
        r'<!\[CDATA\[',                       # CDATA sections
    ]
    
    # Path traversal patterns for comprehensive protection
    PATH_TRAVERSAL_PATTERNS = [
        r'\.\.',                              # Parent directory references
        r'\\+',                               # Multiple backslashes
        r'\/+\.\.+\/',                        # Mixed separators
        r':',                                 # Drive letters
        r'\*',                                # Wildcards
        r'\?',                                # Question marks
        r'["\'<>|]',                          # Dangerous characters
        r'\0',                                # Null bytes
    ]
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r'(\bunion\b\s+\bselect\b)',          # Union select
        r'(\bor\b\s+1=1\b)',                  # OR 1=1
        r'(\band\b\s+1=1\b)',                 # AND 1=1
        r';--',                               # SQL comment
        r'/\*.*?\*/',                         # Block comments
        r'(\bdrop\b\s+\btable\b)',            # Drop table
        r'(\binsert\b\s+\binto\b)',           # Insert into
        r'(\bupdate\b\s+\bset\b)',            # Update set
        r'(\bdelete\b\s+\bfrom\b)',           # Delete from
    ]

    @classmethod
    def validate_and_sanitize_input(cls, 
                                   input_data: Any, 
                                   input_type: str = "text",
                                   strict_mode: bool = True) -> Any:
        """
        Unified input validation and sanitization
        
        Args:
            input_data: Data to validate and sanitize
            input_type: Type of input ('text', 'html', 'json', 'filename', 'email', etc.)
            strict_mode: Enable strict security validation
            
        Returns:
            Validated and sanitized data
            
        Raises:
            SecurityValidationError: If validation fails
        """
        if input_data is None:
            return None
            
        # Handle different input types
        if input_type == "text":
            return cls._validate_and_sanitize_text(input_data, strict_mode)
        elif input_type == "html":
            return cls._validate_and_sanitize_html(input_data, strict_mode)
        elif input_type == "json":
            return cls._validate_and_sanitize_json(input_data, strict_mode)
        elif input_type == "filename":
            return cls._validate_and_sanitize_filename(input_data, strict_mode)
        elif input_type == "email":
            return cls._validate_and_sanitize_email(input_data)
        else:
            return cls._validate_and_sanitize_text(str(input_data), strict_mode)

    @classmethod
    def _validate_and_sanitize_text(cls, text: str, strict_mode: bool = True) -> str:
        """Validate and sanitize plain text input"""
        if not isinstance(text, str):
            raise SecurityValidationError(f"Expected string, got {type(text)}")
            
        # Check for dangerous patterns
        cls._check_dangerous_patterns(text, cls.XSS_PATTERNS, "XSS attack pattern")
        cls._check_dangerous_patterns(text, cls.SQL_INJECTION_PATTERNS, "SQL injection pattern")
        
        # Basic sanitization
        sanitized = text.strip()
        
        # In strict mode, escape all HTML
        if strict_mode:
            sanitized = html.escape(sanitized, quote=True)
            
        return sanitized

    @classmethod
    def _validate_and_sanitize_html(cls, html_content: str, strict_mode: bool = True) -> str:
        """Validate and sanitize HTML content"""
        if not isinstance(html_content, str):
            raise SecurityValidationError(f"Expected string, got {type(html_content)}")
            
        # Check for dangerous patterns
        cls._check_dangerous_patterns(html_content, cls.XSS_PATTERNS, "XSS attack pattern")
        cls._check_dangerous_patterns(html_content, cls.SQL_INJECTION_PATTERNS, "SQL injection pattern")
        
        # Use bleach for HTML sanitization with strict settings
        allowed_tags = ['p', 'br', 'strong', 'b', 'em', 'i', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        allowed_attributes = {
            'a': ['href', 'title', 'rel'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
        }
        
        # In strict mode, be more restrictive
        if strict_mode:
            allowed_tags = ['p', 'br', 'strong', 'b', 'em', 'i']  # Fewer allowed tags
            allowed_attributes = {'a': ['href'], 'img': ['src', 'alt']}  # Fewer attributes
        
        sanitized = bleach.clean(
            html_content,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True,
            protocols=['http', 'https', 'mailto']  # Only safe protocols
        )
        
        # Additional security check
        if len(sanitized) < (len(html_content) * 0.1):
            raise SecurityValidationError("Content appears to contain excessive malicious code")
            
        return sanitized

    @classmethod
    def _validate_and_sanitize_json(cls, json_data: Dict, strict_mode: bool = True) -> Dict:
        """Validate and sanitize JSON data"""
        if not isinstance(json_data, dict):
            raise SecurityValidationError(f"Expected dict, got {type(json_data)}")
            
        sanitized = {}
        for key, value in json_data.items():
            # Validate key format
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
                raise SecurityValidationError(f"Invalid key format: {key}")
                
            # Recursively sanitize nested data
            if isinstance(value, dict):
                sanitized[key] = cls._validate_and_sanitize_json(value, strict_mode)
            elif isinstance(value, list):
                sanitized[key] = [
                    cls._validate_and_sanitize_json(item, strict_mode) if isinstance(item, dict)
                    else cls._validate_and_sanitize_text(str(item), strict_mode)
                    for item in value
                ]
            elif isinstance(value, str):
                sanitized[key] = cls._validate_and_sanitize_text(value, strict_mode)
            else:
                sanitized[key] = value
                
        return sanitized

    @classmethod
    def _validate_and_sanitize_filename(cls, filename: str, strict_mode: bool = True) -> str:
        """Validate and sanitize filename input"""
        if not isinstance(filename, str):
            raise SecurityValidationError(f"Expected string, got {type(filename)}")
            
        # Check for path traversal patterns
        cls._check_dangerous_patterns(filename, cls.PATH_TRAVERSAL_PATTERNS, "Path traversal pattern")
        
        # Additional filename validation
        if len(filename) > 255:
            raise SecurityValidationError("Filename too long")
            
        # Remove any directory components
        safe_filename = filename.split('/')[-1].split('\\')[-1]
        
        # Check for reserved names on Windows
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        if safe_filename.upper() in reserved_names:
            raise SecurityValidationError(f"Reserved filename: {safe_filename}")
            
        return safe_filename

    @classmethod
    def _validate_and_sanitize_email(cls, email: str) -> str:
        """Validate and sanitize email input"""
        if not isinstance(email, str):
            raise SecurityValidationError(f"Expected string, got {type(email)}")
            
        email = email.strip().lower()
        
        # Enhanced email validation
        email_pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        
        if not re.match(email_pattern, email):
            raise SecurityValidationError("Invalid email format")
            
        if len(email) > 254:
            raise SecurityValidationError("Email address too long")
            
        # Additional security checks
        dangerous_patterns = [r'<', r'>', r'(', r')', r';', r',', r':', r'\\', r'\'', r'"']
        for pattern in dangerous_patterns:
            if re.search(pattern, email):
                raise SecurityValidationError("Invalid characters in email")
                
        return email

    @classmethod
    def _check_dangerous_patterns(cls, content: str, patterns: List[str], error_type: str):
        """Check content against dangerous patterns"""
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                raise SecurityValidationError(f"{error_type} detected: {pattern}")

    @classmethod
    def validate_request_headers(cls, headers: Dict[str, str]) -> bool:
        """Validate HTTP headers for security"""
        dangerous_headers = [
            'x-forwarded-host', 'x-original-url', 'x-rewrite-url',
            'host', 'origin', 'referer'
        ]
        
        for header_name in dangerous_headers:
            if header_name.lower() in headers:
                header_value = headers[header_name.lower()]
                # Check for path traversal in header values
                if re.search(r'\.\./', header_value):
                    raise SecurityValidationError(f"Path traversal detected in header: {header_name}")
                    
        return True

    @classmethod
    def validate_url(cls, url: str) -> bool:
        """Validate URL for security"""
        if not isinstance(url, str):
            raise SecurityValidationError("URL must be a string")
            
        dangerous_protocols = ['javascript:', 'vbscript:', 'data:', 'file:', 'ftp:']
        for protocol in dangerous_protocols:
            if url.lower().startswith(protocol):
                raise SecurityValidationError(f"Dangerous protocol detected: {protocol}")
                
        # Check for path traversal
        if re.search(r'\.\./', url):
            raise SecurityValidationError("Path traversal detected in URL")
            
        return True


# Convenience functions for easy integration
def validate_input(data: Any, input_type: str = "text", strict_mode: bool = True) -> Any:
    """
    Convenience function for input validation
    
    Args:
        data: Data to validate
        input_type: Type of input
        strict_mode: Enable strict validation
        
    Returns:
        Validated data
    """
    return InputValidationMiddleware.validate_and_sanitize_input(data, input_type, strict_mode)


def sanitize_text(text: str, strict_mode: bool = True) -> str:
    """Convenience function for text sanitization"""
    return InputValidationMiddleware._validate_and_sanitize_text(text, strict_mode)


def sanitize_html(html_content: str, strict_mode: bool = True) -> str:
    """Convenience function for HTML sanitization"""
    return InputValidationMiddleware._validate_and_sanitize_html(html_content, strict_mode)