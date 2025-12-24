#!/usr/bin/env python3
"""
Test Configuration for Security Tests
Sets up environment variables required for testing without compromising security
"""
import os
from typing import Dict, Any


def setup_test_environment() -> None:
    """Set up environment variables for security testing"""
    test_secrets = {
        'JWT_SECRET_KEY': 'test-jwt-secret-key-for-security-testing-only',
        'SECRET_KEY': 'test-secret-key-for-security-testing-only',
        'FLASK_SECRET_KEY': 'test-flask-secret-key-for-security-testing-only',
        'SESSION_SECRET_KEY': 'test-session-secret-key-for-security-testing',
        'CSRF_SECRET_KEY': 'test-csrf-secret-key-for-security-testing',
        'FLASH_SECRET_KEY': 'test-flash-secret-key-for-security-testing'
    }
    
    # Set test environment variables
    for key, value in test_secrets.items():
        os.environ[key] = value
    
    print("[OK] Test environment variables configured for security testing")


def cleanup_test_environment() -> None:
    """Clean up test environment variables"""
    test_secrets = [
        'JWT_SECRET_KEY',
        'SECRET_KEY',
        'FLASK_SECRET_KEY',
        'SESSION_SECRET_KEY',
        'CSRF_SECRET_KEY',
        'FLASH_SECRET_KEY'
    ]
    
    for key in test_secrets:
        os.environ.pop(key, None)
    
    print("[OK] Test environment variables cleaned up")


def validate_test_environment() -> Dict[str, Any]:
    """Validate that test environment is properly configured"""
    required_vars = ['JWT_SECRET_KEY', 'SECRET_KEY', 'FLASK_SECRET_KEY', 'SESSION_SECRET_KEY', 'CSRF_SECRET_KEY', 'FLASH_SECRET_KEY']
    missing_vars = []
    configured_vars = []
    
    for var in required_vars:
        if var in os.environ and os.environ[var]:
            configured_vars.append(var)
        else:
            missing_vars.append(var)
    
    return {
        'configured': configured_vars,
        'missing': missing_vars,
        'is_ready': len(missing_vars) == 0
    }


if __name__ == "__main__":
    # Test the configuration
    print("[SETUP] Setting up test environment...")
    setup_test_environment()
    
    validation = validate_test_environment()
    print(f"Configured variables: {validation['configured']}")
    print(f"Missing variables: {validation['missing']}")
    print(f"Environment ready: {validation['is_ready']}")
    
    print("\n[CLEANUP] Cleaning up test environment...")
    cleanup_test_environment()
    
    validation_after = validate_test_environment()
    print(f"After cleanup - Configured: {validation_after['configured']}")
    print(f"After cleanup - Missing: {validation_after['missing']}")
    print(f"After cleanup - Ready: {validation_after['is_ready']}")