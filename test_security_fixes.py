#!/usr/bin/env python3
"""
Security fixes validation test
This script tests the specific security vulnerabilities that were fixed.
"""

import os
import sys
import tempfile
import unittest
from io import BytesIO
from unittest.mock import patch, MagicMock

# Add the app directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_database_migration_safety():
    """Test that the database migration function is now safe"""
    print("Testing database migration safety...")
    
    try:
        from app.models import migrate_db
        
        # Test that migration fails in production environment
        with patch.dict(os.environ, {'FLASK_ENV': 'production', 'DEBUG': 'false'}):
            try:
                migrate_db()
                print("❌ FAIL: Migration should not run in production")
                return False
            except ValueError as e:
                if "production" in str(e):
                    print("✅ PASS: Migration correctly refuses to run in production")
                else:
                    print(f"❌ FAIL: Wrong error message: {e}")
                    return False
        
        # Test that migration requires explicit confirmation
        with patch.dict(os.environ, {'DEBUG': 'true', 'CONFIRM_DESTRUCTIVE_MIGRATION': 'false'}):
            try:
                migrate_db()
                print("❌ FAIL: Migration should require explicit confirmation")
                return False
            except ValueError as e:
                if "confirmation" in str(e):
                    print("✅ PASS: Migration correctly requires explicit confirmation")
                else:
                    print(f"❌ FAIL: Wrong error message: {e}")
                    return False
                    
        print("✅ PASS: Database migration safety checks implemented")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error testing migration safety: {e}")
        return False

def test_file_upload_security():
    """Test file upload security validation"""
    print("Testing file upload security...")
    
    try:
        from app.handlers.settings_handlers import upload_logo
        from app.handlers.plant_handlers import upload_plant_images
        
        # Test file size validation
        large_file = MagicMock()
        large_file.filename = "test.jpg"
        large_file.mimetype = "image/jpeg"
        large_file.tell.return_value = 20 * 1024 * 1024  # 20 MB
        large_file.seek = MagicMock()
        
        result = upload_logo(large_file)
        if result["success"] or "size" not in result.get("error", "").lower():
            print("❌ FAIL: File size validation not working")
            return False
        print("✅ PASS: File size validation working")
        
        # Test file type validation
        bad_file = MagicMock()
        bad_file.filename = "test.exe"
        bad_file.mimetype = "application/exe"
        bad_file.tell.return_value = 1024  # Small file
        bad_file.seek = MagicMock()
        
        result = upload_logo(bad_file)
        if result["success"] or "type" not in result.get("error", "").lower():
            print("❌ FAIL: File type validation not working")
            return False
        print("✅ PASS: File type validation working")
        
        print("✅ PASS: File upload security validation implemented")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error testing file upload security: {e}")
        return False

def test_removed_debugging():
    """Test that debugging print statements were removed"""
    print("Testing removal of debugging statements...")
    
    try:
        # Check auth.py for removed debug prints
        with open('app/blueprints/auth.py', 'r') as f:
            auth_content = f.read()
            
        # Look for actual debugging patterns, not just "print(" which could be in other contexts
        debug_patterns = [
            'print(f"LOGIN DEBUG',
            'print(f"=== LOGIN ROUTE',
            'LOGIN DEBUG:',
            'print("LOGIN DEBUG',
            'print("=== LOGIN ROUTE'
        ]
        found_debug = []
        for pattern in debug_patterns:
            if pattern in auth_content:
                found_debug.append(pattern)
        
        if found_debug:
            print(f"❌ FAIL: Found debugging statements: {found_debug}")
            return False
        
        print("✅ PASS: Debugging statements removed from authentication")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error checking debugging removal: {e}")
        return False

def test_endpoint_protection():
    """Test that endpoints are properly protected"""
    print("Testing endpoint protection...")
    
    try:
        # Check diagnostics.py for login_required decorator
        with open('app/blueprints/diagnostics.py', 'r') as f:
            diag_content = f.read()
            
        if '@login_required' not in diag_content:
            print("❌ FAIL: Diagnostics endpoint not protected with @login_required")
            return False
        
        if 'current_user.is_admin' not in diag_content:
            print("❌ FAIL: Diagnostics endpoint not checking admin privileges")
            return False
        
        # Check admin.py for admin_required decorator on test endpoint
        with open('app/blueprints/admin.py', 'r') as f:
            admin_content = f.read()
            
        # Look for the diagnostics_test_api function with admin_required
        if 'def diagnostics_test_api' in admin_content:
            # Find the function and check if it has @admin_required before it
            lines = admin_content.split('\n')
            for i, line in enumerate(lines):
                if 'def diagnostics_test_api' in line:
                    # Check previous lines for @admin_required
                    found_decorator = False
                    for j in range(max(0, i-5), i):
                        if '@admin_required' in lines[j]:
                            found_decorator = True
                            break
                    if not found_decorator:
                        print("❌ FAIL: diagnostics_test_api not protected with @admin_required")
                        return False
                    break
        
        print("✅ PASS: Endpoints properly protected")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error checking endpoint protection: {e}")
        return False

def test_commented_imports_removed():
    """Test that commented imports were removed"""
    print("Testing removal of commented imports...")
    
    try:
        # Check sensor_handlers.py
        with open('app/handlers/sensor_handlers.py', 'r') as f:
            sensor_content = f.read()
            
        if '# import requests #commented out' in sensor_content:
            print("❌ FAIL: Commented import still present in sensor_handlers.py")
            return False
        
        print("✅ PASS: Commented imports removed")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error checking commented imports: {e}")
        return False

def test_unused_function_removed():
    """Test that unused check_password function was removed"""
    print("Testing removal of unused functions...")
    
    try:
        # Check auth.py
        with open('app/utils/auth.py', 'r') as f:
            auth_content = f.read()
            
        if 'def check_password(' in auth_content:
            print("❌ FAIL: Unused check_password function still present")
            return False
        
        print("✅ PASS: Unused functions removed")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error checking unused functions: {e}")
        return False

def main():
    """Run all security fix validation tests"""
    print("🔒 Running Security Fixes Validation Tests")
    print("=" * 50)
    
    tests = [
        test_database_migration_safety,
        test_file_upload_security,
        test_removed_debugging,
        test_endpoint_protection,
        test_commented_imports_removed,
        test_unused_function_removed,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ FAIL: {test.__name__} - {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"✅ PASSED: {passed}")
    print(f"❌ FAILED: {failed}")
    print(f"📊 TOTAL:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All security fixes validated successfully!")
        return True
    else:
        print(f"\n⚠️  {failed} security issues still need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)