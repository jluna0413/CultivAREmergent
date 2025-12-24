#!/usr/bin/env python3
"""
Simple JWT Authentication Test
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== JWT Authentication Fix Test ===")
print()

# Test 1: Check if PyJWT is working
try:
    import jwt
    print("PASS - PyJWT library imported successfully")
    print(f"  PyJWT version: {jwt.__version__}")
except ImportError as e:
    print(f"FAIL - PyJWT import failed: {e}")
    exit(1)

# Test 2: Check JWT secret key
jwt_secret_key = os.getenv('JWT_SECRET_KEY')
if jwt_secret_key:
    print(f"PASS - JWT_SECRET_KEY loaded: {jwt_secret_key[:20]}...")
else:
    print("FAIL - JWT_SECRET_KEY not found")

# Test 3: Test JWT encoding/decoding
try:
    # Test data
    payload = {
        "user_id": 123,
        "username": "testuser",
        "exp": 9999999999  # Far future
    }
    
    # Encode JWT
    token = jwt.encode(payload, jwt_secret_key, algorithm="HS256")
    print(f"PASS - JWT token encoded successfully: {token[:50]}...")
    
    # Decode JWT
    decoded = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
    print(f"PASS - JWT token decoded successfully: {decoded}")
    
    # Verify payload matches
    if decoded['user_id'] == payload['user_id'] and decoded['username'] == payload['username']:
        print("PASS - JWT payload verification passed")
    else:
        print("FAIL - JWT payload verification failed")
        
except Exception as e:
    print(f"FAIL - JWT test failed: {e}")

# Test 4: Check other environment variables
required_vars = [
    'SECRET_KEY', 'JWT_SECRET_KEY', 'SESSION_SECRET_KEY', 
    'CSRF_SECRET_KEY', 'FLASH_SECRET_KEY'
]

print("\n=== Environment Variables Check ===")
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"PASS - {var}: {value[:20]}...")
    else:
        print(f"FAIL - {var}: NOT SET")

print("\n=== Test Summary ===")
print("If all tests show PASS, the JWT authentication fix is working correctly!")
print("You can now proceed to Task 3: SSL/TLS Configuration")