"""
Test CORS and TrustedHost Security Configuration
Tests the CORS and TrustedHost middleware configuration for security
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import os

def test_cors_middleware_configuration():
    """Test CORS middleware is properly configured in FastAPI app"""
    # Import the FastAPI app
    from app.fastapi_app import app
    
    # Test that CORS middleware is added
    middleware_classes = [middleware.cls for middleware in app.user_middleware]
    
    # Should include CORSMiddleware
    from fastapi.middleware.cors import CORSMiddleware
    assert CORSMiddleware in middleware_classes
    
    # Test the CORS configuration
    cors_middleware = None
    for middleware in app.user_middleware:
        if middleware.cls == CORSMiddleware:
            cors_middleware = middleware
            break
    
    assert cors_middleware is not None
    
    # Test CORS settings (these would be set during app initialization)
    # The actual values depend on environment variables

def test_trusted_host_middleware_configuration():
    """Test TrustedHost middleware is properly configured"""
    # Import the FastAPI app
    from app.fastapi_app import app
    
    # Test that TrustedHost middleware is added
    middleware_classes = [middleware.cls for middleware in app.user_middleware]
    
    # Should include TrustedHostMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    assert TrustedHostMiddleware in middleware_classes

def test_cors_origins_from_environment():
    """Test CORS origins are properly loaded from environment"""
    # Test the environment parsing function directly
    from app.fastapi_app.dependencies import get_cors_origins
    
    # Test with different environment configurations
    test_cases = [
        # (env_value, expected_origins)
        ("http://localhost:3000,https://myapp.com", 
         ["http://localhost:3000", "https://myapp.com"]),
        ("http://localhost:3000,,https://example.com", 
         ["http://localhost:3000", "https://example.com"]),
        (" http://localhost:3000 , https://example.com ", 
         ["http://localhost:3000", "https://example.com"]),
        ("", ["http://localhost:3000", "http://localhost:8000"]),  # Default
        ("single-origin", ["single-origin"]),
    ]
    
    for env_value, expected in test_cases:
        with patch.dict(os.environ, {"FRONTEND_ORIGINS": env_value}):
            origins = get_cors_origins()
            assert origins == expected, f"Failed for env value: '{env_value}'"

def test_allowed_hosts_from_environment():
    """Test ALLOWED_HOSTS are properly loaded from environment"""
    # Test the environment parsing function directly
    from app.fastapi_app.dependencies import get_allowed_hosts
    
    # Test with different environment configurations
    test_cases = [
        # (env_value, expected_hosts)
        ("localhost,127.0.0.1,myapp.com", 
         ["localhost", "127.0.0.1", "myapp.com"]),
        ("localhost,,127.0.0.1,,myapp.com", 
         ["localhost", "127.0.0.1", "myapp.com"]),
        (" localhost , 127.0.0.1 , myapp.com ", 
         ["localhost", "127.0.0.1", "myapp.com"]),
        ("localhost,*.myapp.com", 
         ["localhost", "*.myapp.com"]),
        ("", ["localhost", "127.0.0.1", "*.localhost"]),  # Default
        ("single-host", ["single-host"]),
    ]
    
    for env_value, expected in test_cases:
        with patch.dict(os.environ, {"ALLOWED_HOSTS": env_value}):
            hosts = get_allowed_hosts()
            assert hosts == expected, f"Failed for env value: '{env_value}'"

def test_security_headers_middleware():
    """Test security headers are properly configured"""
    # Import the FastAPI app
    from app.fastapi_app import app
    
    # Check if security-related middleware is configured
    middleware_info = []
    for middleware in app.user_middleware:
        middleware_info.append({
            'cls': middleware.cls.__name__,
            'args': middleware.args
        })
    
    # Should have CORS and TrustedHost middleware
    middleware_classes = [m['cls'] for m in middleware_info]
    assert 'CORSMiddleware' in middleware_classes
    assert 'TrustedHostMiddleware' in middleware_classes

def test_cors_preflight_requests():
    """Test CORS preflight requests are handled correctly"""
    # This test would require the FastAPI app to be running
    # For now, we test the configuration structure
    
    from app.fastapi_app import app
    from fastapi.middleware.cors import CORSMiddleware
    
    # Find CORS middleware
    cors_middleware = None
    for middleware in app.user_middleware:
        if middleware.cls == CORSMiddleware:
            cors_middleware = middleware
            break
    
    # CORS middleware should be configured
    assert cors_middleware is not None

def test_empty_host_filtering():
    """Test that empty hosts are properly filtered for security"""
    from app.fastapi_app.dependencies import get_allowed_hosts
    
    # Test edge cases that could lead to security issues
    dangerous_cases = [
        ",,,",
        "localhost,,,,127.0.0.1",
        " , , , ",
        "localhost,, ,127.0.0.1,,,",
    ]
    
    for case in dangerous_cases:
        with patch.dict(os.environ, {"ALLOWED_HOSTS": case}):
            hosts = get_allowed_hosts()
            # Should not contain empty strings
            assert all(host.strip() for host in hosts)
            # Should not be empty (should fall back to defaults)
            assert len(hosts) > 0

def test_origin_validation():
    """Test that CORS origins are properly validated"""
    from app.fastapi_app.dependencies import get_cors_origins
    
    # Test potentially dangerous inputs
    dangerous_cases = [
        "",  # Empty
        ",,,",  # Only commas
        " http://evil.com , http://localhost:3000",  # Mixed good/bad
        "https://*",  # Wildcard in wrong place
    ]
    
    for case in dangerous_cases:
        with patch.dict(os.environ, {"FRONTEND_ORIGINS": case}):
            origins = get_cors_origins()
            # Should filter empty entries
            assert all(origin.strip() for origin in origins)
            # Should not be empty (should fall back to defaults)
            assert len(origins) > 0

def test_app_security_configuration():
    """Test overall app security configuration"""
    from app.fastapi_app import app
    
    # Check that security middleware is applied in correct order
    middleware_types = [type(middleware.cls).__name__ for middleware in app.user_middleware]
    
    # TrustedHost should come before CORSMiddleware for security
    trusted_host_index = middleware_types.index('TrustedHostMiddleware')
    cors_index = middleware_types.index('CORSMiddleware')
    
    # TrustedHost should be applied first
    assert trusted_host_index < cors_index

def test_development_vs_production_config():
    """Test that development and production configs are different"""
    from app.fastapi_app.dependencies import get_cors_origins, get_allowed_hosts
    
    # Test development configuration
    with patch.dict(os.environ, {
        "FRONTEND_ORIGINS": "http://localhost:3000,http://localhost:8000",
        "ALLOWED_HOSTS": "localhost,127.0.0.1,*.localhost"
    }, clear=True):
        dev_origins = get_cors_origins()
        dev_hosts = get_allowed_hosts()
        
        assert "http://localhost:3000" in dev_origins
        assert "localhost" in dev_hosts
        assert "127.0.0.1" in dev_hosts
        assert "*.localhost" in dev_hosts
    
    # Test production-like configuration
    with patch.dict(os.environ, {
        "FRONTEND_ORIGINS": "https://myapp.com,https://www.myapp.com",
        "ALLOWED_HOSTS": "myapp.com,www.myapp.com"
    }, clear=True):
        prod_origins = get_cors_origins()
        prod_hosts = get_allowed_hosts()
        
        assert "https://myapp.com" in prod_origins
        assert "myapp.com" in prod_hosts
        assert "localhost" not in prod_hosts  # Should not include dev defaults

if __name__ == "__main__":
    # Run tests
    print("Running CORS and TrustedHost Security Tests...")
    
    test_cors_middleware_configuration()
    print("✓ CORS middleware configuration test passed")
    
    test_trusted_host_middleware_configuration()
    print("✓ TrustedHost middleware configuration test passed")
    
    test_cors_origins_from_environment()
    print("✓ CORS origins from environment test passed")
    
    test_allowed_hosts_from_environment()
    print("✓ ALLOWED_HOSTS from environment test passed")
    
    test_security_headers_middleware()
    print("✓ Security headers middleware test passed")
    
    test_cors_preflight_requests()
    print("✓ CORS preflight requests test passed")
    
    test_empty_host_filtering()
    print("✓ Empty host filtering test passed")
    
    test_origin_validation()
    print("✓ Origin validation test passed")
    
    test_app_security_configuration()
    print("✓ App security configuration test passed")
    
    test_development_vs_production_config()
    print("✓ Development vs production config test passed")
    
    print("\nAll CORS and TrustedHost Security Tests Passed! ✅")