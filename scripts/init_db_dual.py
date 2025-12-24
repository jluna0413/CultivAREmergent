import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

import sys
import argparse
from datetime import datetime
from sqlalchemy import select
from app.logger import logger
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Imports moved inside functions to prevent circular dependency/double-init


def init_flask_db():
    """
    Initialize the Flask database with sync SQLAlchemy.
    Creates tables and seeds initial data if not present.
    """
    # Flask imports (moved inside)
    from cultivar_app import create_app
    from app.models import db
    
    # Import models here to avoid circular imports/double definition
    from app.models.base_models import User, Status, Zone, Breeder, Strain, Plant, Sensor, SensorData, BlogPost, LeadMagnet, NewsletterSubscriber, Waitlist, Activity
    from app.models.activities_models import ActivityLog, PlantActivity # Keep old ones if commented out or just remove validation
    # Actually, proceed with refined list
    from app.models.base_models import User, Status, Zone, Breeder, Strain, Plant, Sensor, SensorData, BlogPost, LeadMagnet, NewsletterSubscriber, Waitlist, Activity
    # Note: SystemActivity, ActivityLog, PlantActivity removed as they were missing/unused

    try:
        app = create_app()
        with app.app_context():
            logger.info("Creating Flask database tables...")
            db.create_all()
            logger.info("Flask database tables created or already exist.")

            # Check if any users exist
            if User.query.count() == 0:
                logger.info("Adding initial data to Flask database...")

                # Add default statuses
                statuses = ["Seedling", "Vegetative", "Flowering", "Harvested", "Dead"]
                for s in statuses:
                    if not Status.query.filter_by(status=s).first():
                        db.session.add(Status(status=s))
                db.session.commit()
                logger.info("Default statuses added to Flask.")

                # Add default activity types
                default_activity_types = [
                    {"name": "user_created", "description": "User account created", "category": "system", "is_system": True},
                    {"name": "user_login", "description": "User logged in", "category": "authentication", "is_system": True},
                    {"name": "user_deleted", "description": "User account deleted", "category": "system", "is_system": True},
                    {"name": "admin_status_changed", "description": "Admin status changed for user", "category": "system", "is_system": True},
                    {"name": "password_reset_forced", "description": "Password reset forced for user", "category": "system", "is_system": True},
                    {"name": "plant_added", "description": "New plant added", "category": "plant_management", "is_system": False},
                    {"name": "strain_edited", "description": "Strain details edited", "category": "strain_management", "is_system": False},
                    {"name": "sensor_reading", "description": "Sensor recorded a reading", "category": "sensor_data", "is_system": True},
                    {"name": "clone_created", "description": "Clone created from parent plant", "category": "plant", "is_system": False},
                    {"name": "clone_deleted", "description": "Clone deleted", "category": "plant", "is_system": False},
                    {"name": "plant_activity", "description": "General plant activity", "category": "plant_management", "is_system": False},
                ]
                for at_data in default_activity_types:
                    if not Activity.query.filter_by(name=at_data["name"]).first():
                        db.session.add(Activity(name=at_data["name"]))
                db.session.commit()
                logger.info("Default activity types added to Flask.")

                # Create an admin user
                admin_user = User(
                    username="admin",
                    email="admin@example.com",
                    password_hash=pwd_context.hash("adminpassword"),
                    is_admin=True,
                    is_active=True,
                    is_verified_breeder=True,
                    tier="premium"
                )
                db.session.add(admin_user)
                db.session.commit()
                db.session.refresh(admin_user)
                logger.info("Admin user created in Flask.")

                # Create a regular user
                regular_user = User(
                    username="user",
                    email="user@example.com",
                    password_hash=pwd_context.hash("userpassword"),
                    is_admin=False,
                    is_active=True,
                    is_verified_breeder=False,
                    tier="basic"
                )
                db.session.add(regular_user)
                db.session.commit()
                db.session.refresh(regular_user)
                logger.info("Regular user created in Flask.")

                # Add a sample breeder
                breeder = Breeder(name="Green Genetics", country="USA", website="greengenetics.com", description="Premium cannabis genetics.")
                db.session.add(breeder)
                db.session.commit()
                db.session.refresh(breeder)
                logger.info("Sample breeder added to Flask.")

                # Add a sample strain (replacing Cultivar)
                cultivar = Strain(
                    name="Super Skunk",
                    breeder_id=breeder.id,
                    indica=70,
                    sativa=30,
                    autoflower=False,
                    description="A classic indica-dominant hybrid.",
                    seed_count=10,
                    cycle_time=60,
                    url="https://example.com/superskun",
                    short_description="A classic indica-dominant hybrid."
                )
                db.session.add(cultivar)
                db.session.commit()
                db.session.refresh(cultivar)
                logger.info("Sample strain added to Flask.")

                # Add a sample zone
                zone = Zone(name="Grow Tent 1")
                db.session.add(zone)
                db.session.commit()
                db.session.refresh(zone)
                logger.info("Sample zone added to Flask.")

                # Add a sample plant
                plant = Plant(
                    user_id=admin_user.id,
                    name="Super Skunk #1",
                    description="First plant of Super Skunk.",
                    status_id=1,  # Seedling
                    strain_id=cultivar.id,
                    zone_id=zone.id,
                    start_dt=datetime.utcnow(),
                    autoflower=False
                )
                db.session.add(plant)
                db.session.commit()
                db.session.refresh(plant)
                logger.info("Sample plant added to Flask.")

                # Add a sample blog post
                blog_post = BlogPost(
                    title="The Art of Growing Cannabis",
                    slug="the-art-of-growing-cannabis",
                    content="This is a detailed guide on growing cannabis...",
                    excerpt="A detailed guide for beginners and experienced growers.",
                    author_id=admin_user.id,
                    is_published=True,
                    published_at=datetime.utcnow(),
                    featured_image="/static/images/blog/growing_cannabis.jpg",
                    meta_description="Learn the best practices for growing cannabis.",
                    tags=["growing", "guide", "cannabis"],
                    categories=["cultivation", "guides"]
                )
                db.session.add(blog_post)
                db.session.commit()
                logger.info("Sample blog post added to Flask.")

                # Add a sample lead magnet
                lead_magnet = LeadMagnet(
                    name="Beginner's Grow Guide",
                    description="A comprehensive guide for new growers.",
                    file_path="beginners_grow_guide.pdf",
                    is_active=True
                )
                db.session.add(lead_magnet)
                db.session.commit()
                logger.info("Sample lead magnet added to Flask.")

                # Add a sample newsletter subscriber
                newsletter_subscriber = NewsletterSubscriber(
                    email="subscriber@example.com",
                    subscription_type="email",
                    is_active=True
                )
                db.session.add(newsletter_subscriber)
                db.session.commit()
                logger.info("Sample newsletter subscriber added to Flask.")

                # Add a sample waitlist entry
                waitlist_entry = Waitlist(
                    email="waitlist@example.com",
                    name="John Doe",
                    priority_tier="early_bird",
                    referral_code="XYZ123"
                )
                db.session.add(waitlist_entry)
                db.session.commit()
                logger.info("Sample waitlist entry added to Flask.")

                # Add a sample sensor
                sensor = Sensor(
                    name="Temperature Sensor 1",
                    sensor_type="temperature",
                    unit="°C",
                    zone_id=zone.id,
                    location="Canopy"
                )
                db.session.add(sensor)
                db.session.commit()
                db.session.refresh(sensor)
                logger.info("Sample sensor added to Flask.")

                # Add sample sensor data
                sensor_data = SensorData(
                    sensor_id=sensor.id,
                    value=25.5,
                    created_at=datetime.utcnow()
                )
                db.session.add(sensor_data)
                db.session.commit()
                logger.info("Sample sensor data added to Flask.")

                logger.info("Initial data seeding complete for Flask.")
            else:
                logger.info("Flask database already contains data, skipping initial seeding.")
    except Exception as e:
        logger.error(f"Error initializing Flask database: {e}")
        db.session.rollback()
        raise

async def init_fastapi_db():
    """
    Initialize the FastAPI database with async SQLAlchemy.
    Creates tables and seeds initial data if not present.
    """
    session = None
    session = None
    # FastAPI async imports (moved inside)
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from app.models_async.base import Base, AsyncSessionLocal, async_engine

    session = None
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("FastAPI database tables created or already exist.")

        # Import async models inside function
        from app.models_async.auth import User as AsyncUser
        from app.models_async.grow import Breeder as AsyncBreeder, Cultivar as AsyncCultivar, Plant as AsyncPlant, Status as AsyncStatus, Zone as AsyncZone
        from app.models_async.activities import ActivityType as AsyncActivityType
        from app.models_async.marketing import BlogPost as AsyncBlogPost, LeadMagnet as AsyncLeadMagnet, NewsletterSubscriber as AsyncNewsletterSubscriber, Waitlist as AsyncWaitlist
        from app.models_async.sensors import Sensor as AsyncSensor, SensorData as AsyncSensorData
        # Add UserGenetics to imports
        from app.models_async.user_genetics import UserGenetics
        from app.models_async.sales import SalesTransaction

        async with AsyncSessionLocal() as session:
            # Check if any users exist
            result = await session.execute(select(AsyncUser))
            existing_users = result.first()
            if not existing_users:
                logger.info("Adding initial data to FastAPI database...")

                # Add default activity types
                default_activity_types = [
                    {"name": "user_created", "description": "User account created", "category": "system", "is_system": True},
                    # ... [snipped for brevity] ...
                ]
                
                # Activity seeding logic (using AsyncActivity) - SKIPPED (Model does not exist)
                # ... [snipped loop] ...
                
                await session.commit()


                # Add default statuses
                statuses = ["Seedling", "Vegetative", "Flowering", "Harvested", "Dead"]
                for s in statuses:
                    result = await session.execute(select(AsyncStatus).where(AsyncStatus.status == s))
                    if not result.scalar_one_or_none():
                        session.add(AsyncStatus(status=s))
                await session.commit()
                logger.info("Default statuses added to FastAPI.")

                # Add default activity types
                default_activity_types = [
                    {"name": "user_created", "description": "User account created", "category": "system", "is_system": True},
                    {"name": "user_login", "description": "User logged in", "category": "authentication", "is_system": True},
                    {"name": "user_deleted", "description": "User account deleted", "category": "system", "is_system": True},
                    {"name": "admin_status_changed", "description": "Admin status changed for user", "category": "system", "is_system": True},
                    {"name": "password_reset_forced", "description": "Password reset forced for user", "category": "system", "is_system": True},
                    {"name": "plant_added", "description": "New plant added", "category": "plant_management", "is_system": False},
                    {"name": "strain_edited", "description": "Strain details edited", "category": "strain_management", "is_system": False},
                    {"name": "sensor_reading", "description": "Sensor recorded a reading", "category": "sensor_data", "is_system": True},
                    {"name": "clone_created", "description": "Clone created from parent plant", "category": "plant", "is_system": False},
                    {"name": "clone_deleted", "description": "Clone deleted", "category": "plant", "is_system": False},
                    {"name": "plant_activity", "description": "General plant activity", "category": "plant_management", "is_system": False},
                ]
                for at_data in default_activity_types:
                    result = await session.execute(select(AsyncActivityType).where(AsyncActivityType.name == at_data["name"]))
                    if not result.scalar_one_or_none():
                        session.add(AsyncActivityType(**at_data))
                await session.commit()
                logger.info("Default activity types added to FastAPI.")

                # Create an admin user
                admin_user = AsyncUser(
                    username="admin",
                    email="admin@example.com",
                    password_hash=pwd_context.hash("adminpassword"),
                    is_admin=True,
                    is_active=True,
                    is_verified_breeder=True,
                    tier="premium"
                )
                session.add(admin_user)
                await session.commit()
                await session.refresh(admin_user)
                logger.info("Admin user created in FastAPI.")

                # Create a regular user
                regular_user = AsyncUser(
                    username="user",
                    email="user@example.com",
                    password_hash=pwd_context.hash("userpassword"),
                    is_admin=False,
                    is_active=True,
                    is_verified_breeder=False,
                    tier="basic"
                )
                session.add(regular_user)
                await session.commit()
                await session.refresh(regular_user)
                logger.info("Regular user created in FastAPI.")

                # Add a sample breeder
                breeder = AsyncBreeder(name="Green Genetics", country="USA", website="greengenetics.com", description="Premium cannabis genetics.")
                session.add(breeder)
                await session.commit()
                await session.refresh(breeder)
                logger.info("Sample breeder added to FastAPI.")

                # Add a sample cultivar
                cultivar = AsyncCultivar(
                    name="Super Skunk",
                    breeder_id=breeder.id,
                    indica=70,
                    sativa=30,
                    autoflower=False,
                    description="A classic indica-dominant hybrid.",
                    seed_count=10,
                    cycle_time=60,
                    url="https://example.com/superskun",
                    parent_1="Skunk #1",
                    parent_2="Afghani",
                    lineage_json={"parents": ["Skunk #1", "Afghani"]},
                    seedfinder_id="SSK001",
                    thc_content=20.0,
                    cbd_content=0.5,
                    flowering_type="photoperiod",
                    categories=["hybrid", "indica-dominant"]
                )
                session.add(cultivar)
                await session.commit()
                await session.refresh(cultivar)
                logger.info("Sample cultivar added to FastAPI.")

                # Add a sample zone
                zone = AsyncZone(name="Grow Tent 1")
                session.add(zone)
                await session.commit()
                await session.refresh(zone)
                logger.info("Sample zone added to FastAPI.")

                # Add a sample plant
                plant = AsyncPlant(
                    user_id=admin_user.id,
                    name="Super Skunk #1",
                    description="First plant of Super Skunk.",
                    status_id=1,  # Seedling
                    cultivar_id=cultivar.id,
                    zone_id=zone.id,
                    start_dt=datetime.utcnow(),
                    autoflower=False
                )
                session.add(plant)
                await session.commit()
                await session.refresh(plant)
                logger.info("Sample plant added to FastAPI.")

                # Add a sample blog post
                blog_post = AsyncBlogPost(
                    title="The Art of Growing Cannabis",
                    slug="the-art-of-growing-cannabis",
                    content="This is a detailed guide on growing cannabis...",
                    excerpt="A detailed guide for beginners and experienced growers.",
                    author_id=admin_user.id,
                    is_published=True,
                    published_at=datetime.utcnow(),
                    featured_image="/static/images/blog/growing_cannabis.jpg",
                    meta_description="Learn the best practices for growing cannabis.",
                    tags=["growing", "guide", "cannabis"],
                    categories=["cultivation", "guides"]
                )
                session.add(blog_post)
                await session.commit()
                logger.info("Sample blog post added to FastAPI.")

                # Add a sample lead magnet
                lead_magnet = AsyncLeadMagnet(
                    name="Beginner's Grow Guide",
                    description="A comprehensive guide for new growers.",
                    file_path="beginners_grow_guide.pdf",
                    is_active=True
                )
                session.add(lead_magnet)
                await session.commit()
                logger.info("Sample lead magnet added to FastAPI.")

                # Add a sample newsletter subscriber
                newsletter_subscriber = AsyncNewsletterSubscriber(
                    email="subscriber@example.com",
                    subscription_type="email",
                    is_active=True
                )
                session.add(newsletter_subscriber)
                await session.commit()
                logger.info("Sample newsletter subscriber added to FastAPI.")

                # Add a sample waitlist entry
                waitlist_entry = AsyncWaitlist(
                    email="waitlist@example.com",
                    name="John Doe",
                    priority_tier="early_bird",
                    referral_code="XYZ123"
                )
                session.add(waitlist_entry)
                await session.commit()
                logger.info("Sample waitlist entry added to FastAPI.")

                # Add a sample sensor
                sensor = AsyncSensor(
                    name="Temperature Sensor 1",
                    sensor_type="temperature",
                    unit="°C",
                    zone_id=zone.id,
                    location="Canopy"
                )
                session.add(sensor)
                await session.commit()
                await session.refresh(sensor)
                logger.info("Sample sensor added to FastAPI.")

                # Add sample sensor data
                sensor_data = AsyncSensorData(
                    sensor_id=sensor.id,
                    value=25.5,
                    created_at=datetime.utcnow()
                )
                session.add(sensor_data)
                await session.commit()
                logger.info("Sample sensor data added to FastAPI.")

                logger.info("Initial data seeding complete for FastAPI.")
            else:
                logger.info("FastAPI database already contains data, skipping initial seeding.")
    except Exception as e:
        logger.error(f"Error initializing FastAPI database: {e}")
        if session:
            await session.rollback()
        raise e

def main():
    """
    Main function to handle command-line arguments and initialize the appropriate database(s).
    """
    parser = argparse.ArgumentParser(description="Initialize database for Flask, FastAPI, or both.")
    parser.add_argument('--flask', action='store_true', help='Initialize Flask database')
    parser.add_argument('--fastapi', action='store_true', help='Initialize FastAPI database')
    parser.add_argument('--both', action='store_true', help='Initialize both Flask and FastAPI databases')
    args = parser.parse_args()

    app_mode = os.getenv('APP_MODE', '').lower()

    if args.both or (args.flask and args.fastapi):
        logger.info("Initializing both Flask and FastAPI databases")
        init_flask_db()
        asyncio.run(init_fastapi_db())
    elif args.flask or app_mode == 'flask':
        logger.info("Initializing Flask database")
        init_flask_db()
    elif args.fastapi or app_mode == 'fastapi':
        logger.info("Initializing FastAPI database")
        asyncio.run(init_fastapi_db())
    else:
        logger.error("Specify --flask, --fastapi, or --both, or set APP_MODE environment variable to 'flask' or 'fastapi'")
        sys.exit(1)

if __name__ == '__main__':
    main()