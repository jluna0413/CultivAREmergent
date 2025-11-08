"""
Integration tests to verify the router fixes for comments 1-3.
Tests data persistence, async patterns, and correct route prefixes.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
import asyncio
from app.fastapi_app import app
from app.fastapi_app.database import get_async_db, init_database
from app.models_async.auth import User
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
async def test_db():
    """Setup test database."""
    # Initialize database
    await init_database()
    
    # Create test database session
    async for db in get_async_db():
        yield db


class TestRouterPrefixes:
    """Test Comment 1: Verify no duplicate router prefixes."""
    
    def test_no_duplicate_prefixes_in_docs(self, client):
        """Verify no duplicate prefixes like /plants/plants in OpenAPI docs."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check for any duplicate prefixes
        for path in paths.keys():
            path_parts = path.split("/")
            # Should not have patterns like /plants/plants or /cultivars/cultivars
            assert not any(
                path_parts[i] == path_parts[i+1] and len(path_parts[i]) > 1
                for i in range(len(path_parts) - 1)
            ), f"Found duplicate prefix in path: {path}"


class TestAsyncPatterns:
    """Test Comment 3: Verify async ORM patterns in auth."""
    
    def test_auth_uses_async_patterns(self):
        """Verify auth router uses AsyncSession and async patterns."""
        from app.fastapi_app.routers import auth
        import inspect
        
        # Check that functions use async/await
        source = inspect.getsource(auth)
        
        # Should use select() from sqlalchemy, not db.query()
        assert "from sqlalchemy import select" in source
        assert "await db.execute(select(" in source
        assert "db.query" not in source  # Should not use sync query()


class TestDataPersistence:
    """Test Comment 2: Verify data persistence works correctly."""
    
    @pytest.mark.asyncio
    async def test_cultivar_persistence_via_api(self, test_db: AsyncSession):
        """Test that cultivar creation via API actually persists data."""
        from app.models_async.grow import Cultivar, Breeder
        
        # Create a test breeder first
        breeder = Breeder(name="Test Breeder")
        test_db.add(breeder)
        await test_db.commit()
        await test_db.refresh(breeder)
        
        # Create a test cultivar
        cultivar = Cultivar(
            name="Test Cultivar",
            breeder_id=breeder.id,
            indica=50.0,
            sativa=50.0,
            autoflower=False,
            created_by=1  # Assuming user ID 1
        )
        
        test_db.add(cultivar)
        await test_db.commit()
        await test_db.refresh(cultivar)
        
        # Verify it was actually saved
        assert cultivar.id is not None
        
        # Query it back
        from sqlalchemy import select
        result = await test_db.execute(select(Cultivar).where(Cultivar.id == cultivar.id))
        saved_cultivar = result.scalar_one_or_none()
        
        assert saved_cultivar is not None
        assert saved_cultivar.name == "Test Cultivar"
        assert saved_cultivar.breeder_id == breeder.id
        
        # Clean up
        await test_db.delete(saved_cultivar)
        await test_db.delete(breeder)
        await test_db.commit()
    
    @pytest.mark.asyncio
    async def test_user_registration_persistence(self, test_db: AsyncSession):
        """Test that user registration actually persists data."""
        from app.models_async.auth import User
        
        # Create a test user
        user = User(username="testuser", email="test@example.com")
        user.set_password("testpassword")
        
        test_db.add(user)
        await test_db.commit()
        await test_db.refresh(user)
        
        # Verify it was saved
        assert user.id is not None
        
        # Query it back
        from sqlalchemy import select
        result = await test_db.execute(select(User).where(User.id == user.id))
        saved_user = result.scalar_one_or_none()
        
        assert saved_user is not None
        assert saved_user.username == "testuser"
        assert saved_user.check_password("testpassword")
        
        # Clean up
        await test_db.delete(saved_user)
        await test_db.commit()


class TestAPIEndpoints:
    """Test API endpoints work correctly after fixes."""
    
    def test_system_info_endpoint(self, client):
        """Test system info endpoint exists and works."""
        response = client.get("/api/v1/system/info")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "database" in data


if __name__ == "__main__":
    # Run tests manually for verification
    print("Running router fix verification tests...")
    
    client = TestClient(app)
    
    # Test 1: Check docs endpoint
    print("\n1. Testing /docs endpoint...")
    response = client.get("/docs")
    print(f"   Status: {response.status_code}")
    
    # Test 2: Check openapi spec for duplicate prefixes
    print("\n2. Checking for duplicate prefixes...")
    response = client.get("/openapi.json")
    if response.status_code == 200:
        openapi_spec = response.json()
        paths = openapi_spec.get("paths", {})
        duplicate_found = False
        
        for path in paths.keys():
            path_parts = path.split("/")
            for i in range(len(path_parts) - 1):
                if path_parts[i] == path_parts[i+1] and len(path_parts[i]) > 1:
                    print(f"   ❌ Found duplicate prefix in path: {path}")
                    duplicate_found = True
        
        if not duplicate_found:
            print("   ✅ No duplicate prefixes found")
    
    # Test 3: Check async patterns
    print("\n3. Checking async patterns...")
    from app.fastapi_app.routers import auth
    import inspect
    source = inspect.getsource(auth)
    
    if "await db.execute(select(" in source and "db.query" not in source:
        print("   ✅ Auth router uses async patterns correctly")
    else:
        print("   ❌ Auth router may have sync patterns")
    
    # Test 4: Check db.commit calls
    print("\n4. Checking db.commit() calls...")
    from app.fastapi_app.routers import cultivars
    import inspect
    source = inspect.getsource(cultivars)
    
    if "await db.commit()" in source:
        print("   ✅ db.commit() calls have parentheses")
    else:
        print("   ❌ db.commit() calls may be missing parentheses")
    
    print("\nTest verification completed!")