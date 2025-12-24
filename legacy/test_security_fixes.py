#!/usr/bin/env python3
"""
Security Test Suite
Tests all implemented security fixes
"""

import pytest
from flask import Flask
from security_middleware import SecurityMiddleware, validate_html_safety


class TestSecurityMiddleware:
    """Test cases for security middleware"""
    
    def test_input_sanitization(self):
        """Test input sanitization functionality"""
        # Test XSS prevention
        malicious_input = "<script>alert('xss')</script>"
        sanitized = SecurityMiddleware.sanitize_input(malicious_input)
        assert "<script>" not in sanitized
        assert "<script>" in sanitized
        
        # Test SQL injection prevention
        sql_input = "'; DROP TABLE users; --"
        sanitized = SecurityMiddleware.sanitize_input(sql_input)
        assert "DROP TABLE" not in sanitized
        assert "'" not in sanitized
    
    def test_charset_validation(self):
        """Test charset validation"""
        # Valid charsets
        assert SecurityMiddleware.validate_charset("utf-8") == True
        assert SecurityMiddleware.validate_charset("iso-8859-1") == True
        
        # Invalid charsets
        assert SecurityMiddleware.validate_charset("utf-8<script>") == False
        assert SecurityMiddleware.validate_charset("utf-8'; DROP TABLE") == False
    
    def test_event_handler_detection(self):
        """Test event handler detection in HTML"""
        malicious_html = '<img src="x" onerror="alert(1)">'
        report = SecurityMiddleware.check_event_handlers(malicious_html)
        assert report['has_violations'] == True
        assert len(report['violations']) > 0
        
        safe_html = '<img src="safe-image.jpg">'
        report = SecurityMiddleware.check_event_handlers(safe_html)
        assert report['has_violations'] == False
    
    def test_template_validation(self):
        """Test HTML template validation"""
        # Safe template
        safe_template = "<p>{{ safe_text }}</p>"
        result = validate_html_safety(safe_template)
        assert result['is_safe'] == True
        
        # Unsafe template with event handlers
        unsafe_template = '<button onclick="alert(1)">Click me</button>'
        result = validate_html_safety(unsafe_template)
        assert result['is_safe'] == False
        assert len(result['violations']) > 0


def run_security_tests():
    """Run all security tests"""
    import subprocess
    import sys
    
    print("Running security test suite...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            __file__, 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        print("Test Results:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"ERROR: Failed to run tests: {e}")
        return False


if __name__ == "__main__":
    success = run_security_tests()
    if success:
        print("SUCCESS: All security tests passed!")
    else:
        print("ERROR: Some security tests failed!")
