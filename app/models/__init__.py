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
    Migrate the database schema.
    This function applies any pending migrations to the database.
    """
    from app.models.acinfinity_models import ACInfinityDevice, ACInfinityToken
    from app.models.base_models import (
            Activity,
            Breeder,
            Cultivar,
            Measurement,
            Metric,
            Plant,
            PlantActivity,
            PlantImage,
            Sensor,
            SensorData,
            Settings,
            Status,
            Stream,
            User,
            Zone,
        )
    from app.models.ecowitt_models import EcowittDevice
    from app.models.system_models import SystemActivity

    logger.info("Migrating database schema")

    # Drop all tables (destructive operation - data will be lost!)
    db.drop_all()

    # Create tables
    db.create_all()

    # Check if we need to migrate from SQLite to PostgreSQL
    db_driver = os.getenv("CULTIVAR_DB_DRIVER", "sqlite")
    if db_driver == "postgres":
        # Check if we need to import data from SQLite
        sqlite_path = os.path.join("data", "cultivar.db")
        if os.path.exists(sqlite_path) and User.query.count() == 0:
            logger.info("Migrating data from SQLite to PostgreSQL")
            # This would be implemented in a real migration
            # For now, we'll just log that it would happen
            logger.info("Migration from SQLite to PostgreSQL would happen here")

    logger.info("Database migration completed")


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

    from app.models.base_models import User
    from werkzeug.security import generate_password_hash

    # Ensure session is committed before checking user count
    db.session.commit()

    # Add default admin user if no users exist
    logger.info(f"User count before admin creation: {User.query.count()}")
    if User.query.count() == 0:
        admin_user = User(username='admin', email='admin@example.com', is_admin=True)
        admin_user.password_hash = generate_password_hash('isley') # Default password
        db.session.add(admin_user)
        db.session.commit()
        logger.info("Default admin user created.")

    logger.info("Database initialization completed")


# Import both for backward compatibility
from app.models.base_models import Cultivar

# Explicit backward compatibility alias
Strain = Cultivar
