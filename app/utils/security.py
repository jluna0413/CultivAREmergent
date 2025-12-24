"""
Security utility functions for input sanitization and validation
Protects against SQL injection and other common vulnerabilities
"""

import re
import html
from typing import Union, Optional
from sqlalchemy import text
from datetime import datetime


class SecurityValidationError(Exception):
    """Raised when security validation fails"""
    pass


def sanitize_search_input(search_term: str, max_length: int = 100) -> str:
    """
    Sanitize search input to prevent SQL injection in LIKE queries.
    
    Args:
        search_term: Raw search term from user
        max_length: Maximum allowed length
        
    Returns:
        Sanitized search term safe for SQL LIKE operations
        
    Raises:
        SecurityValidationError: If input fails validation
    """
    if not search_term:
        return ""
    
    # Check length
    if len(search_term) > max_length:
        raise SecurityValidationError(f"Search term exceeds maximum length of {max_length} characters")
    
    # Remove or escape SQL wildcards
    sanitized = re.sub(r'[%_\\]', '', search_term)
    
    # Check for SQL injection patterns
    dangerous_patterns = [
        r';\s*(drop|delete|insert|update|create|alter|exec|execute)',  # SQL commands
        r'--',  # SQL comments
        r'/\*.*?\*/',  # Block comments
        r'union\s+select',  # UNION attacks
        r'script\s*>',  # XSS attempts
        r'javascript:',  # JS protocols
        r'data:',  # Data URIs
        r"'\s+or\s+'",  # OR injection with quotes
        r'(\'|")\s*OR\s*(\'|")',  # ' OR ' pattern
        r';'  # Semicolon is dangerous in search inputs with double quotes
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, search_term, re.IGNORECASE):
            raise SecurityValidationError(f"Dangerous pattern detected in search term")
    
    return sanitized.strip()


def sanitize_sql_like_value(value: str) -> str:
    """
    Escape special characters for SQL LIKE patterns.
    
    Args:
        value: Raw value to escape
        
    Returns:
        Escaped value safe for LIKE operations
    """
    if not value:
        return ""
    
    # Escape SQL wildcards and backslashes
    escaped = (
        value.replace('\\', '\\\\')
             .replace('%', '\\%')
             .replace('_', '\\_')
    )
    
    return escaped


def create_safe_search_condition(column, search_term: str) -> text:
    """
    Create a safe SQL condition for searching text columns.
    
    Args:
        column: SQLAlchemy column to search
        search_term: User search term
        
    Returns:
        SQLAlchemy text condition (safe from injection)
    """
    sanitized = sanitize_search_input(search_term)
    
    if not sanitized:
        # Return a condition that always matches empty search
        return text("1=1")
    
    # Use parameterized query with escaped LIKE value
    escaped_term = sanitize_sql_like_value(sanitized)
    
    # Use SQLAlchemy's text() with proper parameterization
    return column.ilike(f"%{escaped_term}%")


def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return False
    
    # Basic email validation regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email)) and len(email) <= 254


def validate_filename(filename: str) -> bool:
    """
    Validate filename to prevent path traversal attacks.
    STRENGTHENED: Enhanced path traversal protection based on validation findings.
    
    Args:
        filename: Filename to validate
        
    Returns:
        True if filename is safe
    """
    if not filename:
        return False
    
    # COMPREHENSIVE: Check for all path traversal patterns
    dangerous_patterns = [
        r'\.\.',                    # Parent directory references (../)
        r'\\+',                     # Multiple backslashes (\\\\)
        r'\/+\.\.+\/',              # Mixed forward/backward (//..//)
        r':',                       # Drive letters (C:, D:, etc.)
        r'\*',                      # Wildcards (*)
        r'\?',                      # Question marks (?)
        r'\"',                      # Double quotes
        r"'",                      # Single quotes
        r'<',                       # Less than
        r'>',                       # Greater than
        r'\|',                      # Pipe
        r'\0',                      # Null bytes
        r'[%]',                     # URL encoding markers
        r'[&]',                     # Ampersands
        r'[;]',                     # Semicolons
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            return False
    
    # Check filename length
    if len(filename) > 255:
        return False
    
    # Additional validation: ensure no consecutive separators
    if '//' in filename or '\\\\' in filename:
        return False
        
    # Validate against known attack patterns from validation
    attack_patterns = [
        r'\.\.\\\.\.\\\.\.',        # ..\\..\\..
        r'\.\.\/\.\.\/\.\.\/',      # ../../../
        r'\.\.\s+\.\.',              # .. .. (with spaces)
        r'file.*\.\.\.*in.*name',    # file_with_.._in_name patterns
        r'etc[\\/]passwd',          # etc/passwd patterns
        r'windows[\\/]system32',     # Windows system paths
        r'\\device[\\/]harddisk',    # Device paths
    ]
    
    for pattern in attack_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            return False
    
    return True


def sanitize_html_content(content: str) -> str:
    """
    Sanitize HTML content to prevent XSS attacks.
    
    Args:
        content: Raw HTML content
        
    Returns:
        Sanitized HTML content
    """
    if not content:
        return ""
    
    # Basic HTML escaping
    sanitized = html.escape(content, quote=True)
    
    # Remove dangerous HTML tags
    dangerous_tags = [
        'script', 'object', 'embed', 'link', 'style', 'iframe',
        'frame', 'frameset', 'applet', 'base', 'form', 'meta',
        'head', 'html', 'body', 'title'
    ]
    
    for tag in dangerous_tags:
        # Remove opening and closing tags
        sanitized = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(f'<{tag}[^>]*/?>', '', sanitized, flags=re.IGNORECASE)
    
    return sanitized.strip()


def validate_json_data(data: dict, allowed_keys: list = None) -> dict:
    """
    Validate and sanitize JSON data.
    
    Args:
        data: Raw data dictionary
        allowed_keys: List of allowed keys (whitelist)
        
    Returns:
        Validated and sanitized data
        
    Raises:
        SecurityValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise SecurityValidationError("Invalid data type")
    
    # Whitelist approach - only allow specific keys
    if allowed_keys:
        sanitized = {}
        for key, value in data.items():
            if key in allowed_keys:
                if isinstance(value, str):
                    sanitized[key] = value.strip()
                else:
                    sanitized[key] = value
        return sanitized
    
    # Default sanitization
    sanitized = {}
    for key, value in data.items():
        # Validate key format
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
            continue
        
        if isinstance(value, str):
            sanitized[key] = value.strip()
        else:
            sanitized[key] = value
    
    return sanitized


def validate_uploaded_file(file_content: bytes, filename: str, allowed_extensions: list = None) -> bool:
    """
    Validate uploaded file to prevent security issues.
    
    Args:
        file_content: File content in bytes
        filename: Original filename
        allowed_extensions: List of allowed file extensions
        
    Returns:
        True if file is safe
        
    Raises:
        SecurityValidationError: If file is unsafe
    """
    # Validate filename
    if not validate_filename(filename):
        raise SecurityValidationError("Invalid filename")
    
    # Check file size (limit to 10MB)
    if len(file_content) > 10 * 1024 * 1024:
        raise SecurityValidationError("File too large")
    
    # Validate file extension
    if allowed_extensions:
        if '.' not in filename:
            raise SecurityValidationError("File must have an extension")
        
        extension = filename.rsplit('.', 1)[1].lower()
        if extension not in allowed_extensions:
            raise SecurityValidationError(f"File extension '{extension}' not allowed")
    
    # Check for file signature (basic check for common file types)
    if len(file_content) >= 4:
        file_signature = file_content[:4]
        
        # Common dangerous file signatures
        dangerous_signatures = [
            b'\x4D\x5A',  # PE executable (.exe, .dll)
            b'\x7F\x45\x4C\x46',  # ELF executable (Linux binaries)
            b'\xCA\xFE\xBA\xBE',  # Mach-O executable (Mac binaries)
        ]
        
        if file_signature in dangerous_signatures:
            raise SecurityValidationError("Executable files not allowed")
    
    return True


def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    if not api_key:
        return False
    
    # Basic API key validation (alphanumeric and specific characters)
    api_key_pattern = r'^[a-zA-Z0-9\-_]+$'
    return bool(re.match(api_key_pattern, api_key)) and len(api_key) >= 32


def validate_token(token: str) -> bool:
    """Validate JWT-like token format"""
    if not token:
        return False
    
    # Basic token format validation
    token_pattern = r'^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$'
    return bool(re.match(token_pattern, token))