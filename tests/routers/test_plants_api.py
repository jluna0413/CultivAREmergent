import pytest
from httpx import AsyncClient
from app.fastapi_app.main import app
from app.fastapi_app.dependencies import get_plant_repository, require_login
from app.repositories.sql.plant_repository import SQLPlantRepository
from app.models_async.base import Base
from app.models_async.auth import User
from app.models_async.grow import Status, Cultivar, Breeder
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import StaticPool

# Setup in-memory SQLite for testing with StaticPool to keep data alive across sessions
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db_session():
    # Use StaticPool so the in-memory DB persists for all connections from this engine
    engine = create_async_engine(
        DATABASE_URL, 
        echo=False, 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        # Seed dependencies
        user = User(id=1, username="testuser", password_hash="hash", email="test@example.com")
        status_obj = Status(id=1, status="Veg")
        breeder = Breeder(id=1, name="Test Breeder")
        session.add_all([user, status_obj, breeder])
        await session.flush()
        
        cultivar = Cultivar(id=1, name="Test Strain", breeder_id=breeder.id)
        session.add(cultivar)
        await session.commit()
        
        yield session
    
    await engine.dispose()

@pytest.fixture
def override_dependencies(db_session):
    async def override_get_repo():
        return SQLPlantRepository(db_session)
    
    async def override_require_login():
        class MockUser:
            id = 1
            username = "testuser"
            is_admin = False
        return MockUser()

    app.dependency_overrides[get_plant_repository] = override_get_repo
    app.dependency_overrides[require_login] = override_require_login
    yield
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_plant_api_flow(override_dependencies):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1. Create Plant
        response = await ac.post("/api/v2/plants/api/create", data={
            "name": "API Test Plant",
            "status_id": 1,
            "cultivar_id": 1,
            "is_clone": False
        }, follow_redirects=True) # Follow redirect to GET
        
        assert response.status_code == 200
        data = response.json().get("data")
        assert data is not None
        plant_id = data["id"]
        assert data["name"] == "API Test Plant"
        
        # 2. Get Plant
        response = await ac.get(f"/api/v2/plants/api/{plant_id}")
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "API Test Plant"

        # 3. Update Plant
        response = await ac.put(f"/api/v2/plants/api/{plant_id}", json={
            "name": "Updated API Plant", 
            "status_id": 1
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Plant updated successfully"
        
        # Verify update
        response = await ac.get(f"/api/v2/plants/api/{plant_id}")
        assert response.json()["data"]["name"] == "Updated API Plant"

        # 4. Delete Plant
        response = await ac.delete(f"/api/v2/plants/api/{plant_id}")
        assert response.status_code == 200
        
        # Verify Gone
        response = await ac.get(f"/api/v2/plants/api/{plant_id}")
        assert response.status_code == 404
