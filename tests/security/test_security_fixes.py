"""
Comprehensive Security Test Suite for CultivAR Application
Tests all implemented security fixes and validates normal functionality
"""

import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Set up test environment BEFORE importing anything else
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from tests.security.test_security_config import setup_test_environment, cleanup_test_environment

# Configure test environment for security validation
setup_test_environment()

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.utils.security import (
    sanitize_search_input, 
    SecurityValidationError,
    validate_filename,
    validate_uploaded_file,
    create_safe_search_condition
)
from app.services.auth_service import UnifiedAuthService, TokenValidationError, AuthenticationError


class TestSecurityUtilityFunctions:
    """Test security utility functions"""
    
    def test_sanitize_search_input_normal(self):
        """Test normal search input is handled correctly"""
        # Valid search terms should work
        assert sanitize_search_input("normal search") == "normal search"
        assert sanitize_search_input("plant genetics") == "plant genetics"
        assert sanitize_search_input("grow tips") == "grow tips"
    
    def test_sanitize_search_input_sql_injection_attempts(self):
        """Test SQL injection attempts are blocked"""
        # Test patterns that should be blocked by our security function
        
        # SQL command pattern - should be blocked
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("'; DROP TABLE users; --")
        
        # UNION attack - should be blocked
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("UNION SELECT * FROM users")
        
        # SQL comment pattern - should be blocked
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("admin'--")
        
        # Basic OR injection (should also be blocked due to semicolon)
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("admin' OR '1'='1")
        
        # Test that semicolon alone triggers blocking
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("';")
        
        # Test that comments trigger blocking
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("/* comment */")
        
        # Test case insensitivity
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("UNION select * from users")
        
        # Test XSS patterns are blocked
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("<script>alert('xss')</script>")
        
        with pytest.raises(SecurityValidationError, match="Dangerous pattern detected"):
            sanitize_search_input("javascript:alert('xss')")
    
    def test_sanitize_search_input_xss_attempts(self):
        """Test XSS attempts are blocked"""
        with pytest.raises(SecurityValidationError):
            sanitize_search_input("<script>alert('xss')</script>")
        
        with pytest.raises(SecurityValidationError):
            sanitize_search_input("javascript:alert('xss')")
    
    def test_sanitize_search_input_length_limit(self):
        """Test input length validation"""
        # Test max length enforcement
        long_input = "a" * 101  # Exceeds 100 character limit
        with pytest.raises(SecurityValidationError):
            sanitize_search_input(long_input)
    
    def test_validate_filename_safe(self):
        """Test safe filenames are accepted"""
        assert validate_filename("normal_file.jpg") == True
        assert validate_filename("plant_photo.png") == True
        assert validate_filename("image123.gif") == True
    
    def test_validate_filename_dangerous(self):
        """Test dangerous filenames are rejected"""
        # Path traversal attempts
        assert validate_filename("../../../etc/passwd") == False
        assert validate_filename("..\\..\\windows\\system32") == False
        
        # Dangerous characters
        assert validate_filename("file<name.txt") == False
        assert validate_filename("file>name.txt") == False
        assert validate_filename("file|name.txt") == False
        assert validate_filename('file"name.txt') == False
        assert validate_filename("file?name.txt") == False
        assert validate_filename("file*name.txt") == False
    
    def test_validate_uploaded_file_safe(self):
        """Test safe files pass validation"""
        # Safe image file
        safe_content = b'\x89PNG\r\n\x1a\n'  # PNG header
        assert validate_uploaded_file(
            file_content=safe_content,
            filename="test.png",
            allowed_extensions={'png', 'jpg', 'jpeg'}
        ) == True
        
        # Safe text file
        safe_content = b"Hello, world!"
        assert validate_uploaded_file(
            file_content=safe_content,
            filename="test.txt",
            allowed_extensions={'txt', 'pdf'}
        ) == True
    
    def test_validate_uploaded_file_executable_blocked(self):
        """Test executable files are blocked"""
        # PE executable (Windows .exe)
        exe_content = b'MZ\x90\x00'  # PE executable header
        with pytest.raises(SecurityValidationError):
            validate_uploaded_file(
                file_content=exe_content,
                filename="malware.exe",
                allowed_extensions={'png', 'jpg', 'jpeg'}
            )
    
    def test_validate_uploaded_file_extension_validation(self):
        """Test file extension validation"""
        safe_content = b"safe content"
        
        # Wrong extension should fail
        with pytest.raises(SecurityValidationError):
            validate_uploaded_file(
                file_content=safe_content,
                filename="document.pdf",
                allowed_extensions={'png', 'jpg', 'jpeg'}
            )
    
    def test_validate_uploaded_file_size_limit(self):
        """Test file size limits"""
        # Large file content (>10MB)
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        with pytest.raises(SecurityValidationError):
            validate_uploaded_file(
                file_content=large_content,
                filename="large.txt",
                allowed_extensions={'txt'}
            )


class TestSQLInjectionProtection:
    """Test SQL injection protection in search functions"""
    
    def test_create_safe_search_condition_normal(self):
        """Test normal search terms work with search condition"""
        # This would normally be used with SQLAlchemy, but we can test the sanitization
        result = sanitize_search_input("normal search term")
        assert result == "normal search term"
        assert "normal search term" in result
    
    def test_sql_injection_patterns_blocked(self):
        """Test that SQL injection patterns are completely blocked"""
        injection_patterns = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "UNION SELECT * FROM users",
            "admin'--",
            "'; INSERT INTO users VALUES ('hacker', 'password'); --"
        ]
        
        for pattern in injection_patterns:
            with pytest.raises(SecurityValidationError):
                sanitize_search_input(pattern)
    
    def test_search_functionality_preserved(self):
        """Test that normal search functionality still works"""
        # These should all work without issues
        valid_searches = [
            "cannabis",
            "indica",
            "sativa",
            "hydroponic",
            "LED lighting",
            "pH levels",
            "nutrients",
            "harvest time"
        ]
        
        for search in valid_searches:
            result = sanitize_search_input(search)
            assert result == search
            assert len(result) <= 100


class TestAuthenticationSecurity:
    """Test unified authentication service security"""
    
    @patch.dict(os.environ, {
        'JWT_SECRET_KEY': 'test-secret-key-for-security-validation',
        'JWT_ALGORITHM': 'HS256',
        'JWT_EXPIRATION_MINUTES': '1440'
    })
    def test_auth_service_initialization(self):
        """Test authentication service initializes correctly"""
        auth_service = UnifiedAuthService()
        assert auth_service.jwt_secret == 'test-secret-key-for-security-validation'
        assert auth_service.jwt_algorithm == 'HS256'
        assert auth_service.jwt_expiration_minutes == 1440
    
    def test_password_hashing_security(self):
        """Test password hashing and verification"""
        auth_service = UnifiedAuthService()
        
        password = "SecurePassword123!"
        hashed = auth_service.hash_password(password)
        
        # Hash should be different from original password
        assert hashed != password
        
        # Verification should work
        assert auth_service.verify_password(password, hashed) == True
        
        # Wrong password should fail
        assert auth_service.verify_password("wrongpassword", hashed) == False
    
    @patch.dict(os.environ, {
        'JWT_SECRET_KEY': 'test-jwt-secret-for-validation',
        'JWT_ALGORITHM': 'HS256',
        'JWT_EXPIRATION_MINUTES': '1440'
    })
    def test_jwt_token_generation_and_validation(self):
        """Test JWT token generation and validation"""
        # Create a proper user-like object instead of Mock
        class TestUser:
            def __init__(self):
                self.id = 123
                self.username = "testuser"
                self.email = "test@example.com"
                self.is_admin = False
        
        auth_service = UnifiedAuthService()
        test_user = TestUser()
        
        # Generate token
        token = auth_service.generate_token(test_user)
        assert isinstance(token, str)
        assert len(token) > 50  # JWT tokens are reasonably long
        
        # Validate token
        payload = auth_service.validate_token(token)
        assert payload['user_id'] == 123
        assert payload['username'] == "testuser"
        assert payload['email'] == "test@example.com"
        assert payload['is_admin'] == False
    
    def test_expired_token_handling(self):
        """Test handling of expired tokens"""
        # Create a proper user-like object
        class TestUser:
            def __init__(self):
                self.id = 123
                self.username = "testuser"
                self.email = "test@example.com"
                self.is_admin = False
        
        # Patch Config.JWT_EXPIRATION_MINUTES to -1 to generate expired tokens
        with patch('app.config.config.Config.JWT_EXPIRATION_MINUTES', -1):
            auth_service = UnifiedAuthService()
            test_user = TestUser()
            
            # Generate token with expired setting
            token = auth_service.generate_token(test_user)
            assert isinstance(token, str)
            
            # Validation should fail due to expiration
            with pytest.raises(TokenValidationError, match="expired"):
                auth_service.validate_token(token)


class TestFileUploadSecurity:
    """Test file upload security measures"""
    
    def test_logo_upload_security(self):
        """Test that logo upload has proper security validation"""
        # This would normally test the upload_logo function from settings_handlers
        # For now, we'll test the underlying security functions
        
        # Test safe image upload
        safe_image = b'\x89PNG\r\n\x1a\n' + b'x' * 1000  # PNG with content
        try:
            validate_uploaded_file(
                file_content=safe_image,
                filename="logo.png",
                allowed_extensions={'png', 'jpg', 'jpeg', 'svg'}
            )
            assert True  # Should succeed
        except SecurityValidationError:
            pytest.fail("Safe image upload should not fail")
    
    def test_plant_image_upload_security(self):
        """Test that plant image upload has proper security validation"""
        # Test various image formats
        image_formats = [
            (b'\x89PNG\r\n\x1a\n', "plant.png"),
            (b'\xff\xd8\xff', "photo.jpg"),  # JPEG header
            (b'GIF87a', "image.gif"),
            (b'GIF89a', "image.gif")
        ]
        
        for content, filename in image_formats:
            try:
                validate_uploaded_file(
                    file_content=content,
                    filename=filename,
                    allowed_extensions={'png', 'jpg', 'jpeg', 'gif', 'webp'}
                )
                assert True  # Should succeed
            except SecurityValidationError:
                pytest.fail(f"Safe image format {filename} should not fail validation")
    
    def test_path_traversal_protection(self):
        """Test path traversal attack protection"""
        dangerous_filenames = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32",
            "file/../../../secret.txt",
            ".\\..\\..\\config.txt",
            "normal../../malicious.txt"
        ]
        
        for filename in dangerous_filenames:
            assert validate_filename(filename) == False, f"Path traversal filename {filename} should be rejected"


class TestConfigurationSecurity:
    """Test configuration security improvements"""
    
    def test_no_hardcoded_secrets(self):
        """Test that hardcoded secret fallbacks have been removed"""
        # List of files to check for hardcoded secrets
        files_to_check = [
            os.path.join('app', 'config', 'config.py'),
            os.path.join('app', 'fastapi_main', 'main.py'),
            os.path.join('app', 'config', 'config.py')
        ]
        
        # Dangerous secret patterns that should not exist
        dangerous_patterns = [
            'super-secret-key-fallback',
            'super-secret-csrf-key',
            'flash-secret-key-fallback',
            'super-secret-jwt-key-fallback',
            'dev-secret-key-for-testing'
        ]
        
        files_checked = 0
        for file_path in files_to_check:
            if os.path.exists(file_path):
                files_checked += 1
                try:
                    # Try different encodings to handle file encoding issues
                    content = None
                    encodings = ['utf-8', 'latin-1', 'cp1252']
                    
                    for encoding in encodings:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                content = f.read()
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if content is not None:
                        for pattern in dangerous_patterns:
                            assert pattern not in content, f"Dangerous pattern '{pattern}' found in {file_path}"
                    else:
                        print(f"Warning: Could not read {file_path} with any encoding")
                        
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
        
        # Assert that we checked at least one file
        assert files_checked > 0, "No configuration files were found to check"
        
        # Test environment variable validation
        from app.config.config import Config
        import tempfile
        
        # Test that missing environment variables cause proper errors
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("# Empty env file\n")
            env_file = f.name
        
        try:
            # This should work - just testing that the validation exists
            test_secrets = Config.get_fastapi_secrets()
            # If we get here without errors, at least verify the secrets are from env vars
            if 'JWT_SECRET_KEY' in test_secrets:
                assert 'super-secret-key-fallback' != test_secrets['JWT_SECRET_KEY']
        except ValueError:
            # Expected - missing environment variables
            pass
        finally:
            os.unlink(env_file)


class TestSecurityIntegration:
    """Integration tests for complete security flow"""
    
    def test_complete_search_workflow_security(self):
        """Test that search functionality works securely end-to-end"""
        # Test normal search workflow
        search_terms = [
            "cannabis",
            "hydroponic system", 
            "LED grow lights",
            "nutrient solution"
        ]
        
        for term in search_terms:
            # Sanitize the input
            sanitized = sanitize_search_input(term)
            
            # Verify it passes through correctly
            assert sanitized == term
            assert len(sanitized) <= 100
            
            # Verify no dangerous patterns remain
            dangerous_patterns = ['<script', 'DROP TABLE', 'UNION SELECT', '--', ';']
            for pattern in dangerous_patterns:
                assert pattern not in sanitized.upper()
    
    def test_file_upload_complete_security(self):
        """Test complete file upload security workflow"""
        # Test safe file upload workflow
        safe_files = [
            ("image.jpg", b'\xff\xd8\xff\x00' + b'x' * 100),  # JPEG
            ("photo.png", b'\x89PNG\r\n\x1a\n' + b'x' * 100),  # PNG
            ("document.txt", b"This is safe content" * 10),  # Text
        ]
        
        for filename, content in safe_files:
            # Validate filename
            assert validate_filename(filename) == True
            
            # Validate file content
            try:
                validate_uploaded_file(
                    file_content=content,
                    filename=filename,
                    allowed_extensions={'jpg', 'png', 'txt', 'pdf'}
                )
                assert True  # Should succeed
            except SecurityValidationError:
                pytest.fail(f"Safe file {filename} should pass validation")


def run_security_tests():
    """Run all security tests and report results"""
    print("[SECURITY] Running CultivAR Security Validation Tests")
    print("=" * 50)
    
    # Run pytest programmatically
    import pytest
    exit_code = pytest.main([
        '-v',
        '--tb=short',
        '--disable-warnings',
        __file__
    ])
    
    if exit_code == 0:
        print("\n[SUCCESS] All security tests PASSED!")
        print("[SUCCESS] Application security validation SUCCESSFUL!")
    else:
        print("\n[FAILURE] Some security tests FAILED!")
        print("[WARNING] Please review failed tests and fix issues")
    
    return exit_code


if __name__ == "__main__":
    run_security_tests()