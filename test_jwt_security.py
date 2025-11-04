"""
Test JWT Security Implementation
Tests the enhanced JWT validation, rotation, and revocation functionality
"""

import asyncio
import pytest
import datetime
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from jose import jwt
import os

# Test the JWT security functions directly
def test_generate_jti():
    """Test JTI generation produces unique IDs"""
    from app.fastapi_app.dependencies import generate_jti
    
    jti1 = generate_jti()
    jti2 = generate_jti()
    
    assert jti1 != jti2
    assert len(jti1) == 36  # UUID string length
    assert len(jti2) == 36

def test_token_revocation():
    """Test token JTI revocation functionality"""
    from app.fastapi_app.dependencies import (
        add_token_to_revocation, 
        is_token_revoked_by_jti,
        generate_jti
    )
    
    # Test basic revocation
    jti = generate_jti()
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    
    # Token should not be revoked initially
    assert not is_token_revoked_by_jti(jti)
    
    # Add to revocation
    add_token_to_revocation(jti, expiry)
    
    # Token should now be revoked
    assert is_token_revoked_by_jti(jti)

def test_rotated_refresh_tokens():
    """Test refresh token rotation tracking"""
    from app.fastapi_app.dependencies import (
        add_rotated_refresh_token,
        is_refresh_token_rotated,
        generate_jti
    )
    
    # Test basic rotation tracking
    jti = generate_jti()
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    
    # Token should not be rotated initially
    assert not is_refresh_token_rotated(jti)
    
    # Mark as rotated
    add_rotated_refresh_token(jti, expiry)
    
    # Token should now be marked as rotated
    assert is_refresh_token_rotated(jti)

def test_enhanced_jwt_verification():
    """Test enhanced JWT verification with type validation"""
    from app.fastapi_app.dependencies import verify_jwt_token, create_access_token_with_jti
    
    # Create test token
    test_data = {"user_id": 1, "username": "testuser"}
    token = create_access_token_with_jti(test_data)
    
    # Should verify correctly
    payload = verify_jwt_token(token, "access")
    assert payload is not None
    assert payload["user_id"] == 1
    assert payload["username"] == "testuser"
    assert payload["type"] == "access"
    assert "jti" in payload
    
    # Should reject wrong token type
    payload = verify_jwt_token(token, "refresh")
    assert payload is None
    
    # Should reject invalid token
    payload = verify_jwt_token("invalid_token", "access")
    assert payload is None

def test_token_creation_with_jti():
    """Test token creation includes JTI"""
    from app.fastapi_app.dependencies import create_access_token_with_jti, create_refresh_token_with_jti
    
    test_data = {"user_id": 1, "username": "testuser"}
    
    # Test access token creation
    access_token = create_access_token_with_jti(test_data)
    assert access_token is not None
    
    # Decode to verify structure
    from app.fastapi_app.routers.auth import SECRET_KEY, ALGORITHM
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert payload["user_id"] == 1
    assert payload["username"] == "testuser"
    assert payload["type"] == "access"
    assert "jti" in payload
    assert payload["jti"] is not None
    
    # Test refresh token creation
    refresh_token = create_refresh_token_with_jti(test_data)
    assert refresh_token is not None
    
    # Decode to verify structure
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert payload["user_id"] == 1
    assert payload["username"] == "testuser"
    assert payload["type"] == "refresh"
    assert "jti" in payload
    assert payload["jti"] is not None

@pytest.mark.asyncio
async def test_refresh_token_rotation():
    """Test refresh token rotation functionality"""
    from app.fastapi_app.dependencies import rotate_refresh_token
    from app.fastapi_app.dependencies import (
        is_refresh_token_rotated,
        create_refresh_token_with_jti
    )
    
    # Create initial refresh token
    user_data = {"user_id": 1, "username": "testuser"}
    initial_refresh = create_refresh_token_with_jti(user_data)
    
    # Get the JTI from the token
    from app.fastapi_app.routers.auth import SECRET_KEY, ALGORITHM
    payload = jwt.decode(initial_refresh, SECRET_KEY, algorithms=[ALGORITHM])
    initial_jti = payload["jti"]
    
    # Rotate the token
    new_access, new_refresh = await rotate_refresh_token(initial_refresh, user_data)
    
    # Verify new tokens are created
    assert new_access is not None
    assert new_refresh is not None
    assert new_access != initial_refresh
    assert new_refresh != initial_refresh
    
    # Verify old token is marked as rotated
    assert is_refresh_token_rotated(initial_jti)
    
    # Verify new tokens have different JTIs
    new_payload = jwt.decode(new_refresh, SECRET_KEY, algorithms=[ALGORITHM])
    new_jti = new_payload["jti"]
    assert new_jti != initial_jti

def test_cors_origins_parsing():
    """Test CORS origins parsing with empty entry filtering"""
    from app.fastapi_app.dependencies import get_cors_origins
    
    # Test normal parsing
    with patch.dict(os.environ, {"FRONTEND_ORIGINS": "http://localhost:3000,https://example.com"}):
        origins = get_cors_origins()
        assert origins == ["http://localhost:3000", "https://example.com"]
    
    # Test empty entry filtering
    with patch.dict(os.environ, {"FRONTEND_ORIGINS": "http://localhost:3000,,https://example.com,,http://localhost:8000"}):
        origins = get_cors_origins()
        assert origins == ["http://localhost:3000", "https://example.com", "http://localhost:8000"]
    
    # Test whitespace trimming
    with patch.dict(os.environ, {"FRONTEND_ORIGINS": " http://localhost:3000 , https://example.com "}):
        origins = get_cors_origins()
        assert origins == ["http://localhost:3000", "https://example.com"]
    
    # Test empty environment variable (should use defaults)
    with patch.dict(os.environ, {"FRONTEND_ORIGINS": ""}):
        origins = get_cors_origins()
        assert origins == ["http://localhost:3000", "http://localhost:8000"]

def test_allowed_hosts_parsing():
    """Test ALLOWED_HOSTS parsing with empty host filtering"""
    from app.fastapi_app.dependencies import get_allowed_hosts
    
    # Test normal parsing
    with patch.dict(os.environ, {"ALLOWED_HOSTS": "localhost,127.0.0.1,myapp.com"}):
        hosts = get_allowed_hosts()
        assert hosts == ["localhost", "127.0.0.1", "myapp.com"]
    
    # Test empty host filtering
    with patch.dict(os.environ, {"ALLOWED_HOSTS": "localhost,,127.0.0.1,,myapp.com"}):
        hosts = get_allowed_hosts()
        assert hosts == ["localhost", "127.0.0.1", "myapp.com"]
    
    # Test whitespace trimming
    with patch.dict(os.environ, {"ALLOWED_HOSTS": " localhost , 127.0.0.1 , myapp.com "}):
        hosts = get_allowed_hosts()
        assert hosts == ["localhost", "127.0.0.1", "myapp.com"]
    
    # Test wildcard support
    with patch.dict(os.environ, {"ALLOWED_HOSTS": "localhost,*.myapp.com"}):
        hosts = get_allowed_hosts()
        assert hosts == ["localhost", "*.myapp.com"]
    
    # Test empty environment variable (should use defaults)
    with patch.dict(os.environ, {"ALLOWED_HOSTS": ""}):
        hosts = get_allowed_hosts()
        assert hosts == ["localhost", "127.0.0.1", "*.localhost"]

def test_security_dependencies_import():
    """Test that security dependencies are properly imported"""
    from app.fastapi_app import dependencies
    
    # Check that required functions exist
    assert hasattr(dependencies, 'get_current_user')
    assert hasattr(dependencies, 'get_current_admin_user')
    assert hasattr(dependencies, 'verify_jwt_token')
    assert hasattr(dependencies, 'rotate_refresh_token')
    assert hasattr(dependencies, 'get_cors_origins')
    assert hasattr(dependencies, 'get_allowed_hosts')

def test_jwt_claims_structure():
    """Test that JWT tokens have correct claims structure"""
    from app.fastapi_app.dependencies import create_access_token_with_jti
    from app.fastapi_app.routers.auth import SECRET_KEY, ALGORITHM
    from jose import jwt
    
    test_data = {"user_id": 1, "username": "testuser", "is_admin": True}
    token = create_access_token_with_jti(test_data)
    
    # Decode and verify claims
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Required claims
    assert "user_id" in payload
    assert "username" in payload
    assert "exp" in payload
    assert "type" in payload
    assert "jti" in payload
    
    # Claim values
    assert payload["user_id"] == 1
    assert payload["username"] == "testuser"
    assert payload["type"] == "access"
    assert isinstance(payload["jti"], str)
    assert len(payload["jti"]) > 0

if __name__ == "__main__":
    # Run tests
    print("Running JWT Security Tests...")
    
    test_generate_jti()
    print("✓ JTI generation test passed")
    
    test_token_revocation()
    print("✓ Token revocation test passed")
    
    test_rotated_refresh_tokens()
    print("✓ Rotated refresh tokens test passed")
    
    test_enhanced_jwt_verification()
    print("✓ Enhanced JWT verification test passed")
    
    test_token_creation_with_jti()
    print("✓ Token creation with JTI test passed")
    
    # Test async function
    asyncio.run(test_refresh_token_rotation())
    print("✓ Refresh token rotation test passed")
    
    test_cors_origins_parsing()
    print("✓ CORS origins parsing test passed")
    
    test_allowed_hosts_parsing()
    print("✓ ALLOWED_HOSTS parsing test passed")
    
    test_security_dependencies_import()
    print("✓ Security dependencies import test passed")
    
    test_jwt_claims_structure()
    print("✓ JWT claims structure test passed")
    
    print("\nAll JWT Security Tests Passed! ✅")