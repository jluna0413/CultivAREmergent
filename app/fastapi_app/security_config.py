"""
FastAPI Security Configuration Module
Handles production security settings, environment validation, and security best practices
"""

import os
import secrets
import logging
from typing import Optional, Dict, Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from pathlib import Path

logger = logging.getLogger(__name__)

class SecurityConfig:
    """Production security configuration handler"""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development").lower()
        self.is_production = self.environment == "production"
        self.is_staging = self.environment == "staging"
        self.is_development = self.environment == "development"
        
        # Core security settings
        self.jwt_secret_key = self._get_jwt_secret_key()
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_access_expire = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.jwt_refresh_expire = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        
        # OIDC / Keycloak Settings
        self.oidc_issuer = os.getenv("OIDC_ISSUER", "http://localhost:8080/realms/cultivar")
        self.oidc_client_id = os.getenv("OIDC_CLIENT_ID", "cultivar-backend")
        self.oidc_jwks_url = os.getenv("OIDC_JWKS_URL", f"{self.oidc_issuer}/protocol/openid-connect/certs")
        self.oidc_algorithms = os.getenv("OIDC_ALGORITHMS", "RS256").split(",")
        
        # Database security
        self.database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./cultivar.db")
        self.database_ssl = os.getenv("DATABASE_SSL", "false").lower() == "true"
        
        # SSL/TLS settings
        self.ssl_cert_path = os.getenv("SSL_CERT_PATH")
        self.ssl_key_path = os.getenv("SSL_KEY_PATH")
        self.force_https = os.getenv("FORCE_HTTPS", "false").lower() == "true"
        self.ssl_verify_mode = os.getenv("SSL_VERIFY_MODE", "required")
        
        # Rate limiting
        self.rate_limit = int(os.getenv("RATE_LIMIT", "100"))
        self.rate_window = int(os.getenv("RATE_WINDOW", "60"))
        
        # CORS settings
        self.cors_origins = self._parse_cors_origins()
        
        # Security headers
        self.enable_csp = os.getenv("ENABLE_CSP", "true").lower() == "true"
        self.enable_hsts = os.getenv("ENABLE_HSTS", "true").lower() == "true"
        self.hsts_max_age = int(os.getenv("HSTS_MAX_AGE", "31536000"))
        self.enable_xframe = os.getenv("ENABLE_XFRAME_OPTIONS", "true").lower() == "true"
        self.enable_xcontent = os.getenv("ENABLE_XCONTENT_TYPE_OPTIONS", "true").lower() == "true"
        self.enable_referrer = os.getenv("ENABLE_REFERRER_POLICY", "true").lower() == "true"
        
        # External services
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.jti_redis_url = os.getenv("JTI_REDIS_URL", self.redis_url)
        self.session_secret_key = os.getenv("SESSION_SECRET_KEY", self.jwt_secret_key)
        
        # API settings
        self.api_docs_enabled = os.getenv("API_DOCS_ENABLED", "false").lower() == "true"
        self.api_redoc_enabled = os.getenv("API_REDOC_ENABLED", "false").lower() == "true"
        
        # Audit and monitoring
        self.enable_audit = os.getenv("ENABLE_AUDIT_LOG", "true").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Validation
        self._validate_config()
    
    def _get_jwt_secret_key(self) -> str:
        """Get and validate JWT secret key"""
        secret = os.getenv("JWT_SECRET_KEY")
        if not secret:
            if self.is_production:
                raise ValueError("JWT_SECRET_KEY is required in production")
            else:
                # Generate temporary key for development
                secret = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
                logger.warning("Generated temporary JWT secret key for development")
        return secret
    
    def _parse_cors_origins(self) -> list:
        """Parse CORS origins from environment"""
        origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "")
        if not origins_str:
            if self.is_production:
                return ["https://cultivar-app.com", "https://www.cultivar-app.com"]
            elif self.is_staging:
                return ["https://staging.cultivar-app.com"]
            else:
                return ["http://localhost:3000", "http://localhost:8080", "*"]
        
        return [origin.strip() for origin in origins_str.split(",")]
    
    def _validate_config(self) -> None:
        """Validate security configuration"""
        errors = []
        
        # Production-specific validations
        if self.is_production:
            if not self.jwt_secret_key or len(self.jwt_secret_key) < 32:
                errors.append("JWT_SECRET_KEY must be at least 32 characters in production")
            
            if self.force_https and not self.ssl_cert_path:
                errors.append("SSL_CERT_PATH required when FORCE_HTTPS is enabled")
            
            if not self.database_url.startswith(("postgresql", "mysql")):
                errors.append("Production database should use PostgreSQL or MySQL")
            
            if not self.cors_origins or "*" in self.cors_origins:
                errors.append("CORS_ALLOWED_ORIGINS must be specific in production")
        
        # General validations
        if self.rate_limit <= 0:
            errors.append("RATE_LIMIT must be positive")
        
        if self.rate_window <= 0:
            errors.append("RATE_WINDOW must be positive")
        
        if errors:
            for error in errors:
                logger.error(f"Security configuration error: {error}")
            raise ValueError("Invalid security configuration")
    
    def get_security_headers(self) -> Dict[str, str]:
        """Generate security headers"""
        headers = {}
        
        if self.enable_hsts:
            headers["Strict-Transport-Security"] = f"max-age={self.hsts_max_age}; includeSubDomains"
        
        if self.enable_xframe:
            headers["X-Frame-Options"] = "DENY"
        
        if self.enable_xcontent:
            headers["X-Content-Type-Options"] = "nosniff"
        
        if self.enable_referrer:
            headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return headers
    
    def get_csp_policy(self, nonce: Optional[str] = None) -> str:
        """Generate Content Security Policy"""
        if not self.enable_csp:
            return ""
        
        policy = {
            "default-src": ["'self'"],
            "script-src": ["'self'"],
            "style-src": ["'self'"],
            "font-src": ["'self'"],
            "img-src": ["'self'", "data:"],
            "connect-src": ["'self'"],
            "object-src": ["'none'"],
            "base-uri": ["'self'"],
            "form-action": ["'self'"],
            "frame-ancestors": ["'none'"],
        }
        
        # Development adjustments
        if self.is_development:
            policy["script-src"].extend(["'unsafe-inline'", "'unsafe-eval'"])
            policy["style-src"].extend(["'unsafe-inline'"])
            policy["connect-src"].extend(["ws:", "wss:"])
            policy["img-src"].append("https:")
        
        # Add nonce to script-src if provided
        if nonce:
            policy["script-src"] = [f"'self'", f"'nonce-{nonce}'"] + [
                src for src in policy["script-src"] if src not in ["'self'", f"'nonce-{nonce}'"]
            ]
        
        # Format policy
        return "; ".join([f"{key} {' '.join(value)}" for key, value in policy.items()])
    
    def get_allowed_hosts(self) -> list:
        """Get list of allowed hosts for production"""
        if self.is_production:
            return [
                "cultivar-app.com",
                "www.cultivar-app.com",
                "api.cultivar-app.com",
                "admin.cultivar-app.com"
            ]
        elif self.is_staging:
            return [
                "staging.cultivar-app.com",
                "staging-api.cultivar-app.com"
            ]
        else:
            return ["*"]  # Allow all in development
    
    def should_require_https(self) -> bool:
        """Check if HTTPS should be required"""
        return self.force_https and self.is_production
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        config = {
            "url": self.database_url,
            "ssl_mode": "require" if self.database_ssl else "disable"
        }
        return config
    
    def validate_environment_file(self) -> bool:
        """Validate that all required environment variables are set for production"""
        if not self.is_production:
            return True
        
        required_vars = [
            "JWT_SECRET_KEY",
            "DATABASE_URL",
            "REDIS_URL"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            return False
        
        return True
    
    def generate_secure_key(self, length: int = 32) -> str:
        """Generate a secure random key"""
        return base64.urlsafe_b64encode(secrets.token_bytes(length)).decode()
    
    def hash_password(self, password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
        """Hash a password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        hashed = kdf.derive(password.encode())
        return base64.b64encode(hashed).decode(), base64.b64encode(salt).decode()
    
    def verify_password(self, password: str, hashed: str, salt: str) -> bool:
        """Verify a password against its hash"""
        try:
            salt_bytes = base64.b64decode(salt.encode())
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt_bytes,
                iterations=100000,
            )
            
            kdf.verify(password.encode(), base64.b64decode(hashed.encode()))
            return True
        except Exception:
            return False

# Global security configuration instance
security_config = SecurityConfig()

# Security validation decorators
def require_production_config(func):
    """Decorator to ensure function runs only in production with proper config"""
    def wrapper(*args, **kwargs):
        if not security_config.is_production:
            raise RuntimeError("This function requires production environment")
        if not security_config.validate_environment_file():
            raise RuntimeError("Production environment validation failed")
        return func(*args, **kwargs)
    return wrapper

def validate_ssl_config():
    """Validate SSL/TLS configuration"""
    if security_config.is_production and security_config.force_https:
        if not security_config.ssl_cert_path or not security_config.ssl_key_path:
            cert_path = Path(security_config.ssl_cert_path or "/etc/ssl/certs/cultivar.crt")
            key_path = Path(security_config.ssl_key_path or "/etc/ssl/private/cultivar.key")
            
            if not cert_path.exists():
                raise FileNotFoundError(f"SSL certificate not found: {cert_path}")
            if not key_path.exists():
                raise FileNotFoundError(f"SSL private key not found: {key_path}")
            
            logger.info("SSL configuration validated")

def init_security_monitoring():
    """Initialize security monitoring and alerting"""
    if security_config.enable_audit:
        logger.info("Audit logging enabled")
        logger.info(f"Security level: {security_config.environment}")
        logger.info(f"Rate limiting: {security_config.rate_limit} requests per {security_config.rate_window} seconds")
        logger.info(f"HTTPS enforcement: {security_config.should_require_https()}")

# Initialize security monitoring
init_security_monitoring()