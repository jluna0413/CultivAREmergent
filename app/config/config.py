"""
Configuration settings for the CultivAR application.
Supports both Flask and FastAPI frameworks for dual-stack operation.
"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the application."""

    # Shared settings (used by both Flask and FastAPI)
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("CULTIVAR_PORT", 5000))

    # Database settings (shared)
    DB_DRIVER = os.getenv("CULTIVAR_DB_DRIVER", "sqlite")
    DB_HOST = os.getenv("CULTIVAR_DB_HOST", "localhost")
    DB_PORT = os.getenv("CULTIVAR_DB_PORT", "5432")
    DB_USER = os.getenv("CULTIVAR_DB_USER")
    DB_PASSWORD = os.getenv("CULTIVAR_DB_PASSWORD")
    DB_NAME = os.getenv("CULTIVAR_DB_NAME", "cultivardb")

    # SQLite database path (shared)
    SQLITE_DB_PATH = os.getenv(
        "SQLITE_DB_PATH",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "cultivar.db",
        ),
    )

    # Upload settings (shared)
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Sensor settings (shared)
    POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 300))  # 5 minutes
    STREAM_GRAB_INTERVAL = int(os.getenv("STREAM_GRAB_INTERVAL", 3600))  # 1 hour

    # Guest mode (shared)
    GUEST_MODE = os.getenv("GUEST_MODE", "False").lower() == "true"

    # SSL/TLS Configuration (shared)
    SSL_ENABLED = os.getenv("SSL_ENABLED", "False").lower() == "true"
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "/path/to/certificate.pem")
    SSL_KEY_PATH = os.getenv("SSL_KEY_PATH", "/path/to/private_key.pem")

    # Default lists (shared)
    Activities = []
    Metrics = []
    Statuses = []
    Zones = []
    Strains = []
    Breeders = []

    # Default settings (shared)
    DEFAULT_SETTINGS = {
        "accent_color": "#4CAF50",
        "email_address": "",
        "polling_interval": 60,
        "data_retention": 30,
        "acinfinity_username": "",
        "acinfinity_password": "",
        "ecowitt_api_key": "",
        "ecowitt_application_key": "",
        "ecowitt_mac": "",
        "backup_time": "02:00",
        "backup_retention": 7,
        "backup_location": "./backups",
    }

    # FastAPI-specific settings
    FASTAPI_PORT = int(os.getenv('FASTAPI_PORT', 8000))
    
    # Critical security settings - NO FALLBACKS ALLOWED for production
    @classmethod
    def get_fastapi_secrets(cls):
        """Get FastAPI secrets with proper validation (no hardcoded fallbacks)."""
        import os
        
        session_key = os.getenv('SESSION_SECRET_KEY')
        csrf_key = os.getenv('CSRF_SECRET_KEY')
        flash_key = os.getenv('FLASH_SECRET_KEY')
        jwt_key = os.getenv('JWT_SECRET_KEY')
        
        # Validate all required secrets are set
        missing_keys = []
        if not session_key:
            missing_keys.append('SESSION_SECRET_KEY')
        if not csrf_key:
            missing_keys.append('CSRF_SECRET_KEY')
        if not flash_key:
            missing_keys.append('FLASH_SECRET_KEY')
        if not jwt_key:
            missing_keys.append('JWT_SECRET_KEY')
            
        if missing_keys:
            raise ValueError(
                f"Missing required FastAPI secrets in environment variables: {', '.join(missing_keys)}. "
                f"These must be set before starting the application in production."
            )
            
        return {
            'SESSION_SECRET_KEY': session_key,
            'CSRF_SECRET_KEY': csrf_key,
            'FLASH_SECRET_KEY': flash_key,
            'JWT_SECRET_KEY': jwt_key
        }
    
    # For backward compatibility - these will use the validated values
    SESSION_SECRET_KEY = None  # Will be populated by get_fastapi_secrets() if needed
    CSRF_SECRET_KEY = None
    FLASH_SECRET_KEY = None
    JWT_SECRET_KEY = None
    
    FRONTEND_ORIGINS = os.getenv('FRONTEND_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(',')
    JWT_ALGORITHM = "RS256"
    with open("private_key.pem", "rb") as f:
        JWT_PRIVATE_KEY = f.read()
    with open("public_key.pem", "rb") as f:
        JWT_PUBLIC_KEY = f.read()
    JWT_EXPIRATION_MINUTES = int(os.getenv('JWT_EXPIRATION_MINUTES', 1440))  # 24 hours

    @classmethod
    def get_database_uri(cls):
        """
        Get the database URI based on the configured driver.

        Returns:
            str: The database URI.
        """
        if cls.DB_DRIVER == "sqlite":
            return f"sqlite:///{cls.SQLITE_DB_PATH}"
        else:  # postgres
            return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

    @classmethod
    def get_async_database_uri(cls):
        """
        Get the async database URI based on the configured driver.
        Used by FastAPI for async database operations.

        Returns:
            str: The async database URI.
        """
        if cls.DB_DRIVER == "sqlite":
            return f"sqlite+aiosqlite:///{cls.SQLITE_DB_PATH}"
        else:  # postgres
            return f"postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

    @classmethod
    def is_fastapi_mode(cls):
        """
        Check if the application is running in FastAPI mode.

        Returns:
            bool: True if APP_MODE is set to 'fastapi', False otherwise.
        """
        return os.getenv('APP_MODE', '').lower() == 'fastapi'

    @classmethod
    def ensure_upload_folder(cls):
        """
        Ensure that the upload folder exists.
        """
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)

        # Create subdirectories
        os.makedirs(os.path.join(cls.UPLOAD_FOLDER, "plants"), exist_ok=True)
        os.makedirs(os.path.join(cls.UPLOAD_FOLDER, "streams"), exist_ok=True)
        os.makedirs(os.path.join(cls.UPLOAD_FOLDER, "logos"), exist_ok=True)

    def __init__(self):
        if not self.DEBUG:
            self.validate_production_settings()

    @classmethod
    def validate_production_settings(cls):
        """
        Validate that critical settings are set when not in debug mode.
        Includes validation for both Flask and FastAPI specific secrets.
        """
        if not cls.DEBUG:
            if not cls.SECRET_KEY:
                raise ValueError("SECRET_KEY must be set in production environment.")
            if cls.DB_DRIVER != "sqlite":
                if not cls.DB_USER:
                    raise ValueError("CULTIVAR_DB_USER must be set in production environment for non-sqlite databases.")
                if not cls.DB_PASSWORD:
                    raise ValueError("CULTIVAR_DB_PASSWORD must be set in production environment for non-sqlite databases.")
            # FastAPI-specific validations only
            if cls.is_fastapi_mode():
                if not cls.JWT_SECRET_KEY:
                    raise ValueError("JWT_SECRET_KEY must be set in production environment for FastAPI.")
                if not cls.SESSION_SECRET_KEY:
                    raise ValueError("SESSION_SECRET_KEY must be set in production environment for FastAPI.")
                if not cls.CSRF_SECRET_KEY:
                    raise ValueError("CSRF_SECRET_KEY must be set in production environment for FastAPI.")
                if not cls.FLASH_SECRET_KEY:
                    raise ValueError("FLASH_SECRET_KEY must be set in production environment for FastAPI.")