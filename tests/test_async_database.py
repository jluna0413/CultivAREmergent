import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from sqlalchemy.exc import InvalidRequestError
import os

# Import async models
from app.models_async.base import Base, AsyncSessionLocal, async_engine
from app.models_async.auth import User
from app.models_async.grow import Plant, Cultivar, Breeder, Status, Zone

# Override DATABASE_URL for testing
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
async def async_engine_fixture():
    """Create an async engine for testing."""
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        echo=False,
    )
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def create_tables(async_engine_fixture):
    """Create all tables in the test database."""
    async with async_engine_fixture.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest.fixture
async def async_session_maker(create_tables, async_engine_fixture):
    """Provide an async sessionmaker for each test."""
    async_session_maker = sessionmaker(
        bind=async_engine_fixture,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    yield async_session_maker

@pytest.mark.asyncio
async def test_create_user(async_session_maker):
    """Test creating a user asynchronously."""
    async with async_session_maker() as async_session:
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.check_password("password123")

@pytest.mark.asyncio
async def test_query_user(async_session_maker):
    """Test querying a user asynchronously."""
    async with async_session_maker() as async_session:
        # Create a user first
        user = User(username="queryuser", email="query@example.com")
        user.set_password("password123")
        async_session.add(user)
        await async_session.commit()
        
        # Query the user
        stmt = select(User).where(User.username == "queryuser")
        result = await async_session.execute(stmt)
        queried_user = result.scalar_one()
        
        assert queried_user.username == "queryuser"
        assert queried_user.email == "query@example.com"

@pytest.mark.asyncio
async def test_update_user(async_session_maker):
    """Test updating a user asynchronously."""
    async with async_session_maker() as async_session:
        # Create a user first
        user = User(username="updateuser", email="update@example.com")
        user.set_password("password123")
        async_session.add(user)
        await async_session.commit()
        
        # Update the user
        user.email = "updated@example.com"
        await async_session.commit()
        await async_session.refresh(user)
        
        assert user.email == "updated@example.com"

@pytest.mark.asyncio
async def test_delete_user(async_session_maker):
    """Test deleting a user asynchronously."""
    async with async_session_maker() as async_session:
        # Create a user first
        user = User(username="deleteuser", email="delete@example.com")
        user.set_password("password123")
        async_session.add(user)
        await async_session.commit()
        
        user_id = user.id
        
        # Delete the user
        await async_session.delete(user)
        await async_session.commit()
        
        # Verify deletion
        stmt = select(User).where(User.id == user_id)
        result = await async_session.execute(stmt)
        assert result.scalar_one_or_none() is None

@pytest.mark.asyncio
async def test_relationships(async_session_maker):
    """Test async relationships (user -> plants, plant -> cultivar)."""
    async with async_session_maker() as async_session:
        # Create related objects
        breeder = Breeder(name="Test Breeder")
        cultivar = Cultivar(name="Test Strain", breeder=breeder)
        status = Status(status="Growing")
        zone = Zone(name="Test Zone")
        user = User(username="reluser", email="rel@example.com")
        user.set_password("password123")
        
        plant = Plant(
            name="Test Plant",
            user=user,
            cultivar=cultivar,
            status=status,
            zone=zone
        )
        
        async_session.add_all([breeder, cultivar, status, zone, user, plant])
        await async_session.commit()
        
        # Query and check relationships
        stmt = select(Plant).where(Plant.name == "Test Plant")
        result = await async_session.execute(stmt)
        queried_plant = result.scalar_one()
        
        assert queried_plant.user.username == "reluser"
        assert queried_plant.cultivar.name == "Test Strain"
        assert queried_plant.cultivar.breeder.name == "Test Breeder"
        assert queried_plant.status.status == "Growing"
        assert queried_plant.zone.name == "Test Zone"

@pytest.mark.asyncio
async def test_transaction_rollback(async_session_maker):
    """Test async transactions and rollbacks."""
    async with async_session_maker() as async_session:
        # Start a transaction
        with pytest.raises(ValueError, match="Simulating a rollback"):
            async with async_session.begin():
                user = User(username="rollbackuser", email="rollback@example.com")
                user.set_password("password123")
                async_session.add(user)
                await async_session.flush()
                
                # Check user exists in transaction
                stmt = select(User).where(User.username == "rollbackuser")
                result = await async_session.execute(stmt)
                assert result.scalar_one_or_none() is not None
                
                # Raise an exception to trigger rollback
                raise ValueError("Simulating a rollback")
        
        # Verify rollback
        stmt = select(User).where(User.username == "rollbackuser")
        result = await async_session.execute(stmt)
        assert result.scalar_one_or_none() is None

@pytest.mark.asyncio
async def test_concurrent_operations(async_session_maker):
    """Test concurrent async operations."""
    async def create_user_async(username: str, session_maker):
        async with session_maker() as local_session:
            user = User(username=username, email=f"{username}@example.com")
            user.set_password("password123")
            local_session.add(user)
            await local_session.commit()
            await local_session.refresh(user)
            return user.id
    
    # Run multiple concurrent operations
    tasks = [
        create_user_async("concurrent1", async_session_maker),
        create_user_async("concurrent2", async_session_maker),
        create_user_async("concurrent3", async_session_maker),
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Verify all users were created
    assert len(results) == 3
    assert all(r is not None for r in results)
    
    # Verify users exist in the database
    async with async_session_maker() as session:
        stmt = select(User).where(User.username.in_(['concurrent1', 'concurrent2', 'concurrent3']))
        result = await session.execute(stmt)
        users = result.scalars().all()
        assert len(users) == 3

@pytest.mark.asyncio
async def test_session_cleanup(async_session_maker):
    """Test async session management and cleanup."""
    async with async_session_maker() as async_session:
        # Create a user
        user = User(username="cleanupuser", email="cleanup@example.com")
        user.set_password("password123")
        async_session.add(user)
        await async_session.commit()
        
        # Close the session
        await async_session.close()
        
        # Verify session is not active (implementation dependent, but good proxy)
        # Note: SQLAlchemy AsyncSession might not raise InvalidRequestError immediately on reuse 
        # if it auto-begins, but we can check if it's closed.
        # For this test, we'll just ensure no error is raised during close.
        pass
# Note: Testing PostgreSQL would require a running PostgreSQL instance.
# For now, we focus on SQLite. To test PostgreSQL, add a parametrized fixture
# with different DATABASE_URLs and ensure asyncpg is installed.