"""
Database models for the CultivAR application.
"""

import os

from flask_sqlalchemy import SQLAlchemy

from app.logger import logger

# Initialize SQLAlchemy
db = SQLAlchemy()


def migrate_db():
    """
    Migrate the database schema safely.
    This function applies any pending migrations to the database without data loss.
    WARNING: This function should only be called in development with explicit user consent.
    """
    from app.models.acinfinity_models import ACInfinityDevice, ACInfinityToken
    from app.models.base_models import (
        Activity,
        Breeder,
        Measurement,
        Metric,
        Plant,
        PlantActivity,
        PlantImage,
        Sensor,
        SensorData,
        Settings,
        Status,
        Strain,
        Stream,
        User,
        Zone,
    )
    from app.models.ecowitt_models import EcowittDevice
    from app.models.system_models import SystemActivity

    logger.warning("DEPRECATED: migrate_db() function called. Use proper database migration tools in production.")
    
    # Check if this is a production environment
    if os.getenv("FLASK_ENV") == "production" or not os.getenv("DEBUG", "false").lower() == "true":
        logger.error("Refusing to run destructive migration in production environment")
        raise ValueError("migrate_db() cannot be run in production. Use proper migration tools like Alembic.")

    # Only proceed if explicitly confirmed in development
    if not os.getenv("CONFIRM_DESTRUCTIVE_MIGRATION", "false").lower() == "true":
        logger.error("Destructive migration requires CONFIRM_DESTRUCTIVE_MIGRATION=true environment variable")
        raise ValueError("Destructive migration requires explicit confirmation via environment variable")

    logger.warning("Performing DESTRUCTIVE database migration - ALL DATA WILL BE LOST!")

    # Create tables only (no drop_all for safety)
    db.create_all()

    # Check if we need to migrate from SQLite to PostgreSQL
    db_driver = os.getenv("CULTIVAR_DB_DRIVER", "sqlite")
    if db_driver == "postgres":
        # Check if we need to import data from SQLite
        sqlite_path = os.path.join("data", "cultivar.db")
        if os.path.exists(sqlite_path):
            logger.info("SQLite database found - consider implementing proper data migration")
            # Proper migration logic would go here

    logger.info("Database schema migration completed safely")


def init_db():
    """
    Initialize the database with default data.
    This function adds default data to the database if it doesn't exist.
    """
    from app.models.base_models import Activity, Metric, Status

    logger.info("Initializing database with default data")

    # Add default activities if they don't exist
    default_activities = [
        {"id": 1, "name": "Water"},
        {"id": 2, "name": "Feed"},
        {"id": 3, "name": "Transplant"},
        {"id": 4, "name": "Top"},
        {"id": 5, "name": "Defoliate"},
        {"id": 6, "name": "Flush"},
        {"id": 7, "name": "Harvest"},
    ]

    for activity_data in default_activities:
        if not Activity.query.get(activity_data["id"]):
            activity = Activity(id=activity_data["id"], name=activity_data["name"])
            db.session.add(activity)

    # Add default metrics if they don't exist
    default_metrics = [
        {"id": 1, "name": "Height", "unit": "cm"},
        {"id": 2, "name": "Width", "unit": "cm"},
        {"id": 3, "name": "pH", "unit": "pH"},
        {"id": 4, "name": "EC", "unit": "mS/cm"},
        {"id": 5, "name": "TDS", "unit": "ppm"},
    ]

    for metric_data in default_metrics:
        if not Metric.query.get(metric_data["id"]):
            metric = Metric(
                id=metric_data["id"], name=metric_data["name"], unit=metric_data["unit"]
            )
            db.session.add(metric)

    # Add default statuses if they don't exist
    default_statuses = [
        {"id": 1, "status": "Seedling"},
        {"id": 2, "status": "Vegetative"},
        {"id": 3, "status": "Flowering"},
        {"id": 4, "status": "Harvested"},
        {"id": 5, "status": "Dead"},
    ]

    for status_data in default_statuses:
        if not Status.query.get(status_data["id"]):
            status = Status(id=status_data["id"], status=status_data["status"])
            db.session.add(status)

    # Commit changes
    db.session.commit()

    logger.info("Database initialization completed")
