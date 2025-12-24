import asyncio
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models_async.base import Base
from app.models_async.auth import User
from app.models_async.grow import Breeder, Cultivar, Plant, Status, Zone
from app.models_async.marketing import BlogPost, LeadMagnet, NewsletterSubscriber, Waitlist
from app.models_async.sensors import Sensor, SensorData
from app.models_async.activities import ActivityType, ActivityLog, PlantActivity
from app.models_async.hypergraph_mappings import HypergraphStrainMapping, HypergraphBreederMapping, HypergraphCultivarMapping
from app.models_async.breeders import MarketplaceBreeder
from app.logger import logger
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./instance/cultivar.db")

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created or already exist.")

    async with AsyncSessionLocal() as session:
        # Add initial data if tables are empty
        # Check if any users exist
        existing_users = await session.execute(User.__table__.select())
        if not existing_users.first():
            logger.info("Adding initial data...")

            # Add default user statuses
            statuses = ["Seedling", "Vegetative", "Flowering", "Harvested", "Dead"]
            for s in statuses:
                status_obj = await session.execute(select(Status).where(Status.status == s))
                if not status_obj.scalar_one_or_none():
                    session.add(Status(status=s))
            await session.commit()
            logger.info("Default statuses added.")

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
                activity_type_obj = await session.execute(select(ActivityType).where(ActivityType.name == at_data["name"]))
                if not activity_type_obj.scalar_one_or_none():
                    session.add(ActivityType(**at_data))
            await session.commit()
            logger.info("Default activity types added.")

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
            session.add(admin_user)
            await session.commit()
            await session.refresh(admin_user)
            logger.info("Admin user created.")

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
            session.add(regular_user)
            await session.commit()
            await session.refresh(regular_user)
            logger.info("Regular user created.")

            # Add a sample breeder
            breeder = Breeder(name="Green Genetics", country="USA", website="greengenetics.com", description="Premium cannabis genetics.")
            session.add(breeder)
            await session.commit()
            await session.refresh(breeder)
            logger.info("Sample breeder added.")

            # Add a sample cultivar
            cultivar = Cultivar(
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
                flowering_type="photoperiod"
            )
            session.add(cultivar)
            await session.commit()
            await session.refresh(cultivar)
            logger.info("Sample cultivar added.")

            # Add a sample zone
            zone = Zone(name="Grow Tent 1")
            session.add(zone)
            await session.commit()
            await session.refresh(zone)
            logger.info("Sample zone added.")

            # Add a sample plant
            plant = Plant(
                user_id=admin_user.id,
                name="Super Skunk #1",
                description="First plant of Super Skunk.",
                status_id=1, # Seedling
                cultivar_id=cultivar.id,
                zone_id=zone.id,
                start_dt=datetime.utcnow(),
                autoflower=False
            )
            session.add(plant)
            await session.commit()
            await session.refresh(plant)
            logger.info("Sample plant added.")

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
            session.add(blog_post)
            await session.commit()
            logger.info("Sample blog post added.")

            # Add a sample lead magnet
            lead_magnet = LeadMagnet(
                name="Beginner's Grow Guide",
                description="A comprehensive guide for new growers.",
                file_path="beginners_grow_guide.pdf",
                is_active=True
            )
            session.add(lead_magnet)
            await session.commit()
            logger.info("Sample lead magnet added.")

            # Add a sample newsletter subscriber
            newsletter_subscriber = NewsletterSubscriber(
                email="subscriber@example.com",
                subscription_type="email",
                is_active=True
            )
            session.add(newsletter_subscriber)
            await session.commit()
            logger.info("Sample newsletter subscriber added.")

            # Add a sample waitlist entry
            waitlist_entry = Waitlist(
                email="waitlist@example.com",
                name="John Doe",
                priority_tier="early_bird",
                referral_code="XYZ123"
            )
            session.add(waitlist_entry)
            await session.commit()
            logger.info("Sample waitlist entry added.")

            # Add a sample sensor
            sensor = Sensor(
                name="Temperature Sensor 1",
                sensor_type="temperature",
                unit="°C",
                zone_id=zone.id,
                location="Canopy"
            )
            session.add(sensor)
            await session.commit()
            await session.refresh(sensor)
            logger.info("Sample sensor added.")

            # Add sample sensor data
            sensor_data = SensorData(
                sensor_id=sensor.id,
                value=25.5,
                created_at=datetime.utcnow()
            )
            session.add(sensor_data)
            await session.commit()
            logger.info("Sample sensor data added.")

            logger.info("Initial data seeding complete.")
        else:
            logger.info("Database already contains data, skipping initial seeding.")

if __name__ == "__main__":
    asyncio.run(init_db())
