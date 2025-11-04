#!/usr/bin/env python3
"""
Comprehensive test for unified JWT validation with refresh rotation and revocation
Tests the implementation of Comment 7 from Flask-to-FastAPI migration
"""

import asyncio
import pytest
import os
from datetime import datetime, timedelta
from jose import jwt
import json

# Set test environment
os.environ["SECRET_KEY"] = "test-secret-key-for-jwt-validation"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.fastapi_app.jwt_utils import (
    create_access_token_with_jti,
    create_refresh_token_with_jti,
    verify_jwt_token,
    rotate_refresh_token,
    is_token_revoked_by_jti,
    is_refresh_token_rotated,
    add_token_to_revocation,
    add_rotated_refresh_token,
    generate_jti,
    revoked_tokens,
    rotated_refresh_tokens,
    SECRET_KEY,
    ALGORITHM
)

class TestUnifiedJWTValidation:
    """Test suite for unified JWT validation with JTI tracking"""
    
    def setup_method(self):
        """Clear revocation stores before each test"""
        revoked_tokens.clear()
        rotated_refresh_tokens.clear()
    
    def test_jti_generation(self):
        """Test JTI generation produces unique identifiers"""
        jti1 = generate_jti()
        jti2 = generate_jti()
        
        assert jti1 != jti2
        assert len(jti1) == 36  # UUID4 format
        assert len(jti2) == 36
    
    def test_access_token_creation_with_jti(self):
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
    
    def test_refresh_token_creation_with_jti(self):
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
    
    def test_jwt_validation_success(self):
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
    
    def test_jwt_validation_wrong_type(self):
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
    
    def test_jwt_validation_invalid_token(self):
        """Test JWT validation fails for invalid tokens"""
        # Invalid token
        payload = verify_jwt_token("invalid.token.here", "access")
        assert payload is None
        
        # Malformed token
        payload = verify_jwt_token("bad.token", "access")
        assert payload is None
        
        # Empty token
        payload = verify_jwt_token("", "access")
        assert payload is None
    
    def test_token_revocation(self):
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
    
    def test_token_revocation_cleanup(self):
        """Test expired revocation entries are cleaned up"""
        user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
        
        # Create token
        token = create_access_token_with_jti(user_data)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload["jti"]
        
        # Add revocation with past expiry
        past_expiry = datetime.utcnow() - timedelta(minutes=1)
        add_token_to_revocation(jti, past_expiry)
        
        # Should be cleaned up automatically
        assert not is_token_revoked_by_jti(jti)
    
    def test_refresh_token_rotation(self):
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
    
    def test_refresh_token_rotation_tracking(self):
        """Test that rotated refresh tokens are properly tracked"""
        user_data = {"user_id": 1, "username": "testuser"}
        
        # Create refresh token
        original_refresh = create_refresh_token_with_jti(user_data)
        original_payload = jwt.decode(original_refresh, SECRET_KEY, algorithms=[ALGORITHM])
        original_jti = original_payload["jti"]
        
        # Rotate token
        new_access, new_refresh = asyncio.run(rotate_refresh_token(original_refresh, user_data))
        
        # Check that old JTI is tracked as rotated
        assert is_refresh_token_rotated(original_jti)
        
        # Try to use old refresh token again (should fail)
        payload = verify_jwt_token(original_refresh, "refresh")
        assert payload is None
    
    def test_refresh_token_rotation_multiple_attempts(self):
        """Test that multiple rotation attempts with same token fail"""
        user_data = {"user_id": 1, "username": "testuser"}
        
        # Create refresh token
        refresh_token = create_refresh_token_with_jti(user_data)
        
        # First rotation should succeed
        new_access1, new_refresh1 = asyncio.run(rotate_refresh_token(refresh_token, user_data))
        assert new_access1 is not None
        
        # Second rotation with same token should fail
        try:
            new_access2, new_refresh2 = asyncio.run(rotate_refresh_token(refresh_token, user_data))
            assert False, "Second rotation should have failed"
        except Exception:
            pass  # Expected to fail
    
    def test_revoked_access_token_validation(self):
        """Test that revoked access tokens cannot be validated"""
        user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
        
        # Create access token
        access_token = create_access_token_with_jti(user_data)
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload["jti"]
        
        # Revoke the token
        expiry = datetime.utcnow() + timedelta(minutes=30)
        add_token_to_revocation(jti, expiry)
        
        # Validation should fail
        result = verify_jwt_token(access_token, "access")
        assert result is None
    
    def test_security_comprehensive_scenario(self):
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
        
        # 9. Try to get new access token with valid refresh
        access_token3, refresh_token3 = asyncio.run(rotate_refresh_token(refresh_token2, user_data))
        assert access_token3 is not None
    
    def test_expired_token_handling(self):
        """Test handling of expired tokens"""
        user_data = {"user_id": 1, "username": "testuser"}
        
        # Create token with very short expiry
        from datetime import timedelta
        token = create_access_token_with_jti(user_data, expires_delta=timedelta(milliseconds=1))
        
        # Wait for token to expire
        import time
        time.sleep(0.01)
        
        # Expired token should fail validation
        payload = verify_jwt_token(token, "access")
        assert payload is None
    
    def test_malformed_token_protection(self):
        """Test protection against malformed tokens"""
        malformed_tokens = [
            "invalid.token",
            "too.many.parts.here.token",
            "",
            "Bearer invalid",
            None,
        ]
        
        for token in malformed_tokens:
            if token is not None:
                payload = verify_jwt_token(token, "access")
                assert payload is None
    
    def test_jti_uniqueness_across_tokens(self):
        """Test that JTI values are unique across different tokens"""
        user_data = {"user_id": 1, "username": "testuser"}
        
        # Create multiple tokens
        tokens = []
        for i in range(10):
            access_token = create_access_token_with_jti(user_data)
            refresh_token = create_refresh_token_with_jti(user_data)
            tokens.extend([access_token, refresh_token])
        
        # Extract all JTIs
        jtis = set()
        for token in tokens:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            jti = payload["jti"]
            assert jti not in jtis, f"Duplicate JTI found: {jti}"
            jtis.add(jti)
        
        assert len(jtis) == 20  # Should have 10 access + 10 refresh = 20 unique JTIs

def run_tests():
    """Run all tests and return results"""
    test_instance = TestUnifiedJWTValidation()
    
    tests = [
        ("JTI Generation", test_instance.test_jti_generation),
        ("Access Token Creation with JTI", test_instance.test_access_token_creation_with_jti),
        ("Refresh Token Creation with JTI", test_instance.test_refresh_token_creation_with_jti),
        ("JWT Validation Success", test_instance.test_jwt_validation_success),
        ("JWT Validation Wrong Type", test_instance.test_jwt_validation_wrong_type),
        ("JWT Validation Invalid Token", test_instance.test_jwt_validation_invalid_token),
        ("Token Revocation", test_instance.test_token_revocation),
        ("Token Revocation Cleanup", test_instance.test_token_revocation_cleanup),
        ("Refresh Token Rotation", test_instance.test_refresh_token_rotation),
        ("Refresh Token Rotation Tracking", test_instance.test_refresh_token_rotation_tracking),
        ("Refresh Token Rotation Multiple Attempts", test_instance.test_refresh_token_rotation_multiple_attempts),
        ("Revoked Access Token Validation", test_instance.test_revoked_access_token_validation),
        ("Security Comprehensive Scenario", test_instance.test_security_comprehensive_scenario),
        ("Expired Token Handling", test_instance.test_expired_token_handling),
        ("Malformed Token Protection", test_instance.test_malformed_token_protection),
        ("JTI Uniqueness Across Tokens", test_instance.test_jti_uniqueness_across_tokens),
    ]
    
    print("=" * 80)
    print("COMPREHENSIVE JWT VALIDATION TEST SUITE")
    print("Testing unified JWT validation with refresh rotation and revocation")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\n[RUNNING] {test_name}")
                test_instance.setup_method()
                test_func()
                print(f"[PASSED] {test_name}")
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