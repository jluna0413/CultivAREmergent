"""
Configuration settings for the CultivAR application.
"""

import os
#from dotenv import load_dotenv

# Load environment variables
#load_dotenv()

class Config:
    """Configuration class for the application."""

    # Application settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('ISLEY_PORT', 4200))

    # Database settings
    DB_DRIVER = os.getenv('ISLEY_DB_DRIVER', 'sqlite')
    DB_HOST = os.getenv('ISLEY_DB_HOST', 'localhost')
    DB_PORT = os.getenv('ISLEY_DB_PORT', '5432')
    DB_USER = os.getenv('ISLEY_DB_USER', 'cultivar')
    DB_PASSWORD = os.getenv('ISLEY_DB_PASSWORD', 'cultivar')
    DB_NAME = os.getenv('ISLEY_DB_NAME', 'cultivardb')

    # SQLite database path
    SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'data/cultivar.db')

    # Upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Sensor settings
    POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL', 300))  # 5 minutes
    STREAM_GRAB_INTERVAL = int(os.getenv('STREAM_GRAB_INTERVAL', 3600))  # 1 hour

    # Guest mode
    GUEST_MODE = os.getenv('GUEST_MODE', 'False').lower() == 'true'

    # Default lists
    Activities = []
    Metrics = []
    Statuses = []
    Zones = []
    Strains = []
    Breeders = []

    @classmethod
    def get_database_uri(cls):
        """
        Get the database URI based on the configured driver.

        Returns:
            str: The database URI.
        """
        if cls.DB_DRIVER == 'sqlite':
            return f'sqlite:///{cls.SQLITE_DB_PATH}'
        else:  # postgres
            return f'postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'

    @classmethod
    def ensure_upload_folder(cls):
        """
        Ensure that the upload folder exists.
        """
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)

        # Create subdirectories
        os.makedirs(os.path.join(cls.UPLOAD_FOLDER, 'plants'), exist_ok=True)
        os.makedirs(os.path.join(cls.UPLOAD_FOLDER, 'streams'), exist_ok=True)
        os.makedirs(os.path.join(cls.UPLOAD_FOLDER, 'logos'), exist_ok=True)
