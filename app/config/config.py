"""
Configuration settings for the CultivAR application.
"""

import os

# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()


class Config:
    """Configuration class for the application."""

    # Application settings
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("CULTIVAR_PORT", 5000))

    # Database settings
    DB_DRIVER = os.getenv("CULTIVAR_DB_DRIVER", "sqlite")
    DB_HOST = os.getenv("CULTIVAR_DB_HOST", "localhost")
    DB_PORT = os.getenv("CULTIVAR_DB_PORT", "5432")
    DB_USER = os.getenv("CULTIVAR_DB_USER")
    DB_PASSWORD = os.getenv("CULTIVAR_DB_PASSWORD")
    DB_NAME = os.getenv("CULTIVAR_DB_NAME", "cultivardb")

    # SQLite database path
    SQLITE_DB_PATH = os.getenv(
        "SQLITE_DB_PATH",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "cultivar.db",
        ),
    )

    # Upload settings
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Sensor settings
    POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 300))  # 5 minutes
    STREAM_GRAB_INTERVAL = int(os.getenv("STREAM_GRAB_INTERVAL", 3600))  # 1 hour

    # Guest mode
    GUEST_MODE = os.getenv("GUEST_MODE", "False").lower() == "true"

    # SSL/TLS Configuration
    SSL_ENABLED = os.getenv("SSL_ENABLED", "False").lower() == "true"
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "/path/to/certificate.pem")
    SSL_KEY_PATH = os.getenv("SSL_KEY_PATH", "/path/to/private_key.pem")

    # Default lists
    Activities = []
    Metrics = []
    Statuses = []
    Zones = []
    Strains = []
    Breeders = []

    # Default settings
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
        """
        if not cls.DEBUG:
            if not cls.SECRET_KEY:
                raise ValueError("SECRET_KEY must be set in production environment.")
            if cls.DB_DRIVER != "sqlite":
                if not cls.DB_USER:
                    raise ValueError("CULTIVAR_DB_USER must be set in production environment for non-sqlite databases.")
                if not cls.DB_PASSWORD:
                    raise ValueError("CULTIVAR_DB_PASSWORD must be set in production environment for non-sqlite databases.")
