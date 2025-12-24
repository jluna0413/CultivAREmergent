import os
import pytest
import pytest_asyncio
from flask.testing import FlaskClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

# Set up environment variables for testing
os.environ.setdefault('TEST_MODE', '1')
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('SESSION_SECRET_KEY', 'test-session-secret')
os.environ.setdefault('CSRF_SECRET_KEY', 'test-csrf-secret')
os.environ.setdefault('FLASH_SECRET_KEY', 'test-flash-secret')
os.environ.setdefault('FRONTEND_ORIGINS', 'http://localhost:3000,http://localhost:8000')

def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "flask_only: mark test to run only on Flask")
    config.addinivalue_line("markers", "fastapi_only: mark test to run only on FastAPI")
    config.addinivalue_line("markers", "both_stacks: mark test to run on both Flask and FastAPI")

@pytest.fixture(scope="session", autouse=True)
def patch_async_engine():
    """
    Patch the async_engine in app.models_async.base to use StaticPool
    for in-memory SQLite database testing.
    """
    from app.models_async import base
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import StaticPool

    # Create a new engine with StaticPool
    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Patch the engine in base module
    original_engine = base.async_engine
    base.async_engine = test_engine
    
    # Also update AsyncSessionLocal to use the new engine
    base.AsyncSessionLocal.configure(bind=test_engine)

    yield test_engine

    # Restore original engine (though session scope means it doesn't matter much)
    base.async_engine = original_engine
    base.AsyncSessionLocal.configure(bind=original_engine)
    test_engine.sync_engine.dispose()

# Flask fixtures
@pytest.fixture(scope="session")
def flask_app():
    """Create Flask app instance for testing."""
    from cultivar_app import create_app
    app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_flask.db'
    })
    return app

@pytest.fixture(scope="session")
def flask_client(flask_app):
    """Create Flask test client."""
    return flask_app.test_client()

@pytest.fixture(scope="function")
def flask_db(flask_app):
    """Set up Flask database with test data."""
    from app.models import db
    with flask_app.app_context():
        db.create_all()
        # Add test data here if needed
        yield db
        db.session.remove()
        
        # Disable foreign key checks for SQLite to avoid "Can't sort tables for DROP" warning
        from sqlalchemy import text
        if 'sqlite' in str(db.engine.url):
            db.session.execute(text("PRAGMA foreign_keys=OFF"))
            
        db.drop_all()
        
        if 'sqlite' in str(db.engine.url):
            db.session.execute(text("PRAGMA foreign_keys=ON"))

# FastAPI fixtures
@pytest.fixture(scope="session")
def fastapi_app():
    """Create FastAPI app instance for testing."""
    from app.fastapi_app.main import app
    return app

from httpx import AsyncClient, ASGITransport

# ... (imports)

@pytest_asyncio.fixture(scope="session")
async def fastapi_client(fastapi_app):
    """Create FastAPI test client."""
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(scope="session")
async def fastapi_async_db():
    """Set up async database session for FastAPI tests."""
    from app.config.config import Config
    from app.models_async.base import Base, async_engine
    # Import all async models to ensure they are registered with Base.metadata
    from app.models_async import auth, grow, iot, sensors, settings, activities, marketing, blog
    
    # Use the shared engine from base.py to ensure app and tests use the same DB
    engine = async_engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        from sqlalchemy import text
        await conn.execute(text("PRAGMA foreign_keys=OFF"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("PRAGMA foreign_keys=ON"))
    await engine.dispose()

# Shared fixtures
@pytest_asyncio.fixture(scope="function")
async def test_user(flask_db, fastapi_async_db: AsyncSession):
    """Create a test user in both databases."""
    from app.models.base_models import User
    from app.models_async.auth import User as AsyncUser
    from werkzeug.security import generate_password_hash
    
    # Flask user
    flask_user = User(
        username='testuser',
        email='test@example.com',
        password_hash=generate_password_hash('password')
    )
    flask_db.session.add(flask_user)
    flask_db.session.commit()
    
    # FastAPI user (assuming similar structure)
    async_user = AsyncUser(
        username='testuser',
        email='test@example.com',
        password_hash=generate_password_hash('password')
    )
    fastapi_async_db.add(async_user)
    await fastapi_async_db.commit()
    await fastapi_async_db.refresh(async_user)
    
    return flask_user, async_user

@pytest_asyncio.fixture(scope="function")
async def test_plant(flask_db, fastapi_async_db: AsyncSession, test_user):
    """Create a test plant in both databases."""
    from app.models.base_models import Plant, Strain, Zone, Breeder
    from app.models_async.grow import Plant as AsyncPlant, Strain as AsyncStrain, Zone as AsyncZone, Breeder as AsyncBreeder
    from datetime import datetime
    
    flask_user, async_user = test_user
    
    # Flask plant setup
    breeder = Breeder(name='Test Breeder')
    flask_db.session.add(breeder)
    strain = Strain(name='Test Strain', breeder=breeder, indica=50, sativa=50)
    flask_db.session.add(strain)
    zone = Zone(name='Test Zone')
    flask_db.session.add(zone)
    flask_db.session.commit()
    
    flask_plant = Plant(
        name='Test Plant',
        strain=strain,
        zone=zone,
        status_id=1,
        start_dt=datetime.now()
    )
    flask_db.session.add(flask_plant)
    flask_db.session.commit()
    
    # FastAPI plant setup
    async_breeder = AsyncBreeder(name='Test Breeder')
    async_strain = AsyncStrain(name='Test Strain', breeder=async_breeder, indica=50, sativa=50)
    async_zone = AsyncZone(name='Test Zone')
    
    fastapi_async_db.add(async_breeder)
    fastapi_async_db.add(async_strain)
    fastapi_async_db.add(async_zone)
    await fastapi_async_db.flush() # Flush to get IDs for relationships if needed
    
    async_plant = AsyncPlant(
        name='Test Plant',
        user_id=async_user.id,
        cultivar_id=async_strain.id,
        status_id=1,
        zone_id=async_zone.id,
        start_dt=datetime.now()
    )
    
    fastapi_async_db.add(async_plant)
    await fastapi_async_db.commit()
    await fastapi_async_db.refresh(async_plant)
    
    return flask_plant, async_plant

@pytest_asyncio.fixture(scope="function")
async def auth_headers(flask_client, fastapi_client, test_user):
    """Generate authentication headers for API tests."""
    flask_user, async_user = test_user
    
    # Flask auth (assuming login endpoint)
    flask_response = flask_client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)
    flask_headers = {'Cookie': flask_response.headers.get('Set-Cookie', '')}
    
    # FastAPI auth (assuming JWT or similar)
    fastapi_response = await fastapi_client.post('/api/v2/auth/login', json={
        'username': 'testuser',
        'password': 'password'
    })
    fastapi_token = fastapi_response.json().get('access_token', '')
    fastapi_headers = {'Authorization': f'Bearer {fastapi_token}'}
    
    return flask_headers, fastapi_headers

# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_databases(flask_db, fastapi_async_db):
    """Reset databases between tests."""
    yield
    # Cleanup will be handled by the db fixtures' teardown