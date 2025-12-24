
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.models_async.base import get_async_session
from app.models_async.auth import User
from sqlalchemy import select
import logging

# Configure logging to print to stdout
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_users(db):
    # 1. Ensure Admin User
    admin_username = "admin_test"
    result = await db.execute(select(User).where(User.username == admin_username))
    admin = result.scalar_one_or_none()
    
    if not admin:
        logger.info(f"Creating admin user: {admin_username}")
        admin = User(
            username=admin_username,
            email="admin_test@cultivaremergent.com",
            is_admin=True,
            user_type="admin",
            tier="premium",
            is_verified_breeder=True
        )
        admin.set_password("TestUser123!")
        db.add(admin)
    else:
        logger.info(f"Admin user {admin_username} already exists")

    # 2. Ensure Standard User
    user_username = "user_test"
    result = await db.execute(select(User).where(User.username == user_username))
    standard_user = result.scalar_one_or_none()
    
    if not standard_user:
        logger.info(f"Creating standard user: {user_username}")
        standard_user = User(
            username=user_username,
            email="user_test@cultivaremergent.com",
            is_admin=False,
            user_type="user",
            tier="free",
            is_verified_breeder=False
        )
        standard_user.set_password("TestUser123!")
        db.add(standard_user)
    else:
        logger.info(f"Standard user {user_username} already exists")

    await db.commit()

async def main():
    logger.info("Starting user seeding for E2E testing...")
    async for db in get_async_session():
        try:
            await seed_users(db)
            logger.info("✅ User seeding completed successfully!")
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ Error seeding users: {e}")
            raise
        finally:
            await db.close()
            break

if __name__ == "__main__":
    asyncio.run(main())
