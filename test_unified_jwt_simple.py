#!/usr/bin/env python3
"""
Simple test for unified JWT validation with refresh rotation and revocation
Tests the implementation of Comment 7 from Flask-to-FastAPI migration
"""

import asyncio
import os
from datetime import datetime, timedelta
from jose import jwt

# Set test environment
os.environ["SECRET_KEY"] = "test-secret-key-for-jwt-validation"

from app.fastapi_app.jwt_utils import (
    create_access_token_with_jti,
    create_refresh_token_with_jti,
    verify_jwt_token,
    rotate_refresh_token,
    is_token_revoked_by_jti,
    add_token_to_revocation,
    add_rotated_refresh_token,
    generate_jti,
    revoked_tokens,
    rotated_refresh_tokens,
    SECRET_KEY,
    ALGORITHM
)

def test_jti_generation():
    """Test JTI generation produces unique identifiers"""
    jti1 = generate_jti()
    jti2 = generate_jti()
    
    assert jti1 != jti2
    assert len(jti1) == 36  # UUID4 format
    assert len(jti2) == 36
    print("[PASSED] JTI generation produces unique identifiers")

def test_access_token_creation_with_jti():
    """Test access token creation includes JTI"""
    user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
    
    token = create_access_token_with_jti(user_data)
    
    # Decode to verify structure
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert payload["user_id"] == 1
    assert payload["username"] == "testuser"
    assert payload["is_admin"] == False
    assert payload["type"] == "access"
    assert "jti" in payload
    assert payload["jti"] is not None
    assert isinstance(payload["jti"], str)
    print("[PASSED] Access token creation includes JTI")

def test_refresh_token_creation_with_jti():
    """Test refresh token creation includes JTI"""
    user_data = {"user_id": 1, "username": "testuser"}
    
    token = create_refresh_token_with_jti(user_data)
    
    # Decode to verify structure
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert payload["user_id"] == 1
    assert payload["username"] == "testuser"
    assert payload["type"] == "refresh"
    assert "jti" in payload
    assert payload["jti"] is not None
    print("[PASSED] Refresh token creation includes JTI")

def test_jwt_validation_success():
    """Test successful JWT validation"""
    user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
    
    # Create tokens
    access_token = create_access_token_with_jti(user_data)
    refresh_token = create_refresh_token_with_jti(user_data)
    
    # Validate access token
    payload = verify_jwt_token(access_token, "access")
    assert payload is not None
    assert payload["user_id"] == 1
    assert payload["username"] == "testuser"
    
    # Validate refresh token
    payload = verify_jwt_token(refresh_token, "refresh")
    assert payload is not None
    assert payload["user_id"] == 1
    print("[PASSED] JWT validation succeeds for valid tokens")

def test_jwt_validation_wrong_type():
    """Test JWT validation fails for wrong token type"""
    user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
    
    access_token = create_access_token_with_jti(user_data)
    refresh_token = create_refresh_token_with_jti(user_data)
    
    # Try to validate access token as refresh token (should fail)
    payload = verify_jwt_token(access_token, "refresh")
    assert payload is None
    
    # Try to validate refresh token as access token (should fail)
    payload = verify_jwt_token(refresh_token, "access")
    assert payload is None
    print("[PASSED] JWT validation fails for wrong token type")

def test_token_revocation():
    """Test token revocation functionality"""
    user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
    
    # Create token
    token = create_access_token_with_jti(user_data)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    jti = payload["jti"]
    
    # Initially should not be revoked
    assert not is_token_revoked_by_jti(jti)
    
    # Revoke token
    expiry = datetime.utcnow() + timedelta(minutes=30)
    add_token_to_revocation(jti, expiry)
    
    # Now should be revoked
    assert is_token_revoked_by_jti(jti)
    
    # Token validation should fail
    payload = verify_jwt_token(token, "access")
    assert payload is None
    print("[PASSED] Token revocation works correctly")

def test_refresh_token_rotation():
    """Test refresh token rotation functionality"""
    user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
    
    # Create initial tokens
    original_access = create_access_token_with_jti(user_data)
    original_refresh = create_refresh_token_with_jti(user_data)
    
    # Rotate refresh token
    new_access, new_refresh = asyncio.run(rotate_refresh_token(original_refresh, user_data))
    
    # Verify new tokens are created
    assert new_access != original_access
    assert new_refresh != original_refresh
    
    # Verify new tokens are valid
    payload = verify_jwt_token(new_access, "access")
    assert payload is not None
    assert payload["user_id"] == 1
    
    payload = verify_jwt_token(new_refresh, "refresh")
    assert payload is not None
    assert payload["user_id"] == 1
    
    # Verify old refresh token is now invalid (rotated)
    payload = verify_jwt_token(original_refresh, "refresh")
    assert payload is None
    print("[PASSED] Refresh token rotation works correctly")

def test_security_comprehensive_scenario():
    """Test comprehensive security scenario"""
    user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
    
    # 1. User logs in
    access_token1 = create_access_token_with_jti(user_data)
    refresh_token1 = create_refresh_token_with_jti(user_data)
    
    # 2. User makes authenticated requests (access token works)
    assert verify_jwt_token(access_token1, "access") is not None
    
    # 3. User refreshes token (rotation occurs)
    access_token2, refresh_token2 = asyncio.run(rotate_refresh_token(refresh_token1, user_data))
    
    # 4. Old refresh token should not work
    assert verify_jwt_token(refresh_token1, "refresh") is None
    
    # 5. New tokens should work
    assert verify_jwt_token(access_token2, "access") is not None
    assert verify_jwt_token(refresh_token2, "refresh") is not None
    
    # 6. User logs out - revoke access token
    payload = jwt.decode(access_token2, SECRET_KEY, algorithms=[ALGORITHM])
    access_jti = payload["jti"]
    expiry = datetime.utcnow() + timedelta(minutes=30)
    add_token_to_revocation(access_jti, expiry)
    
    # 7. Access token should now fail
    assert verify_jwt_token(access_token2, "access") is None
    
    # 8. But refresh token should still work
    assert verify_jwt_token(refresh_token2, "refresh") is not None
    print("[PASSED] Comprehensive security scenario works")

def run_tests():
    """Run all tests and return results"""
    
    print("=" * 80)
    print("COMPREHENSIVE JWT VALIDATION TEST SUITE")
    print("Testing unified JWT validation with refresh rotation and revocation")
    print("=" * 80)
    
    # Clear revocation stores before tests
    revoked_tokens.clear()
    rotated_refresh_tokens.clear()
    
    tests = [
        ("JTI Generation", test_jti_generation),
        ("Access Token Creation with JTI", test_access_token_creation_with_jti),
        ("Refresh Token Creation with JTI", test_refresh_token_creation_with_jti),
        ("JWT Validation Success", test_jwt_validation_success),
        ("JWT Validation Wrong Type", test_jwt_validation_wrong_type),
        ("Token Revocation", test_token_revocation),
        ("Refresh Token Rotation", test_refresh_token_rotation),
        ("Security Comprehensive Scenario", test_security_comprehensive_scenario),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\n[RUNNING] {test_name}")
            test_func()
            passed += 1
        except Exception as e:
            print(f"[FAILED] {test_name}")
            print(f"   Error: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(tests)*100):.1f}%")
    
    if failed == 0:
        print("\n[SUCCESS] ALL TESTS PASSED! Unified JWT validation is working correctly.")
        print("\n[COMPLETE] Comment 7 Implementation Complete:")
        print("   - Unified JWT validation with JTI tracking")
        print("   - Refresh token rotation with reuse prevention")
        print("   - Token revocation store with expiration")
        print("   - Enhanced security across all protected endpoints")
    else:
        print(f"\n[WARNING] {failed} tests failed. Please review the implementation.")
    
    return passed, failed

if __name__ == "__main__":
    run_tests()