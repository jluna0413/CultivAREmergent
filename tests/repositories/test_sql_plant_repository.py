import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models_async.base import Base
from app.models_async.auth import User
from app.models_async.grow import Status, Cultivar, Breeder
from app.repositories.sql.plant_repository import SQLPlantRepository
from app.repositories.interfaces import PlantCreateDTO, PlantUpdateDTO, ActivityDTO
from datetime import datetime

# Setup in-memory SQLite for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        # Seed dependencies
        user = User(username="testuser", password_hash="hash", email="test@example.com")
        status = Status(status="Veg")
        breeder = Breeder(name="Test Breeder")
        session.add_all([user, status, breeder])
        await session.flush()
        
        cultivar = Cultivar(name="Test Strain", breeder_id=breeder.id)
        session.add(cultivar)
        await session.commit()
        
        # IDs for tests
        # User ID: 1, Status ID: 1, Cultivar ID: 1
        
        yield session
    
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_and_get_plant(db_session):
    repo = SQLPlantRepository(db_session)
    
    # Test Create
    plant_in = PlantCreateDTO(
        user_id=1,
        name="Test Plant",
        status_id=1,
        cultivar_id=1,
        zone_id=None
    )
    created = await repo.create(plant_in)
    
    assert created.id is not None
    assert created.name == "Test Plant"
    assert created.user_id == 1
    
    # Test Get
    fetched = await repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.name == "Test Plant"
    assert fetched.status_name == "Veg"
    assert fetched.strain_name == "Test Strain"

@pytest.mark.asyncio
async def test_update_plant(db_session):
    repo = SQLPlantRepository(db_session)
    
    # Create initial
    plant_in = PlantCreateDTO(user_id=1, name="Old Name", status_id=1)
    created = await repo.create(plant_in)
    
    # Test Update
    update_data = PlantUpdateDTO(name="New Name")
    updated = await repo.update(created.id, update_data)
    
    assert updated.name == "New Name"
    
    # Verify persistence
    fetched = await repo.get_by_id(created.id)
    assert fetched.name == "New Name"

@pytest.mark.asyncio
async def test_delete_plant(db_session):
    repo = SQLPlantRepository(db_session)
    
    plant_in = PlantCreateDTO(user_id=1, name="To Delete", status_id=1)
    created = await repo.create(plant_in)
    
    # Test Delete
    success = await repo.delete(created.id)
    assert success is True
    
    # Verify gone
    fetched = await repo.get_by_id(created.id)
    assert fetched is None

@pytest.mark.asyncio
async def test_record_activity(db_session):
    repo = SQLPlantRepository(db_session)
    
    plant_in = PlantCreateDTO(user_id=1, name="Active Plant", status_id=1)
    created = await repo.create(plant_in)
    
    # Test Activity
    activity_in = ActivityDTO(
        plant_id=created.id,
        activity_type="watering",
        details={"amount": 500, "unit": "ml"},
        timestamp=datetime.now()
    )
    
    logged = await repo.record_activity(created.id, activity_in)
    assert logged.activity_type == "watering"
    assert logged.details["amount"] == 500
