"""
Integration tests for authentication endpoints.
Tests actual API endpoints for login, refresh, logout, and token validation.
"""

import pytest
import os
import sys
from datetime import datetime, timedelta
from typing import AsyncGenerator, Dict, Any
import asyncio
import httpx
from unittest.mock import patch, AsyncMock

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.fastapi_app import app
from app.models_async.auth import User
from app.models_async.base import Base, get_async_session
from app.fastapi_app.jwt_utils import create_access_token_with_jti, create_refresh_token_with_jti


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
async def async_session():
    """Create an async database session for testing"""
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session_local = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session_local() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture
async def test_user(async_session: AsyncSession) -> User:
    """Create a test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        is_admin=False
    )
    user.set_password("password123")
    
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    
    return user


@pytest.mark.asyncio
async def test_login_success(test_client: TestClient, test_user: User):
    """Test successful login"""
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    response = test_client.post("/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800


@pytest.mark.asyncio
async def test_login_invalid_credentials(test_client: TestClient):
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    
    response = test_client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401
    data = response.json()
    assert "Invalid username or password" in data["detail"]


@pytest.mark.asyncio
async def test_login_wrong_password(test_client: TestClient, test_user: User):
    """Test login with wrong password"""
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    
    response = test_client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401
    data = response.json()
    assert "Invalid username or password" in data["detail"]


@pytest.mark.asyncio
async def test_refresh_token_success(test_client: TestClient, test_user: User):
    """Test successful token refresh"""
    # First login to get a refresh token
    login_response = test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    
    # Use the refresh token to get a new access token
    refresh_data = {
        "refresh_token": login_data["refresh_token"]
    }
    
    response = test_client.post("/auth/refresh", json=refresh_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800


@pytest.mark.asyncio
async def test_refresh_token_invalid(test_client: TestClient):
    """Test refresh with invalid token"""
    refresh_data = {
        "refresh_token": "invalid_token"
    }
    
    response = test_client.post("/auth/refresh", json=refresh_data)
    
    assert response.status_code == 401
    data = response.json()
    assert "Invalid refresh token" in data["detail"]


@pytest.mark.asyncio
async def test_logout_success(test_client: TestClient, test_user: User):
    """Test successful logout"""
    # First login to get tokens
    login_response = test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    
    # Logout with refresh token
    logout_data = {
        "refresh_token": login_data["refresh_token"]
    }
    
    response = test_client.post("/auth/logout", json=logout_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Logout successful"


@pytest.mark.asyncio
async def test_logout_without_token(test_client: TestClient, test_user: User):
    """Test logout without providing refresh token"""
    response = test_client.post("/auth/logout")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Logout successful"


@pytest.mark.asyncio
async def test_get_current_user_info(test_client: TestClient, test_user: User):
    """Test getting current user info with valid token"""
    # First login to get token
    login_response = test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    access_token = login_data["access_token"]
    
    # Call endpoint with valid token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/auth/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["is_admin"] is False


@pytest.mark.asyncio
async def test_verify_token_success(test_client: TestClient, test_user: User):
    """Test token verification with valid token"""
    # First login to get token
    login_response = test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    access_token = login_data["access_token"]
    
    # Verify the token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/auth/verify", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["user_id"] == test_user.id
    assert data["username"] == "testuser"
    assert data["is_admin"] is False


@pytest.mark.asyncio
async def test_verify_token_invalid(test_client: TestClient):
    """Test token verification with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = test_client.get("/auth/verify", headers=headers)
    
    assert response.status_code == 401
    data = response.json()
    assert "Invalid or expired token" in data["detail"]


@pytest.mark.asyncio
async def test_change_password_success(test_client: TestClient, test_user: User):
    """Test changing user password successfully"""
    # First login to get token
    login_response = test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    access_token = login_data["access_token"]
    
    # Change password
    change_data = {
        "current_password": "password123",
        "new_password": "newpassword456"
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/auth/change-password", json=change_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Password changed successfully"
    
    # Verify new password works for login
    login_response = test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "newpassword456"
    })
    
    assert login_response.status_code == 200


@pytest.mark.asyncio
async def test_change_password_wrong_current(test_client: TestClient, test_user: User):
    """Test changing password with wrong current password"""
    # First login to get token
    login_response = test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    access_token = login_data["access_token"]
    
    # Try to change password with wrong current password
    change_data = {
        "current_password": "wrongpassword",
        "new_password": "newpassword456"
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/auth/change-password", json=change_data, headers=headers)
    
    assert response.status_code == 400
    data = response.json()
    assert "Current password is incorrect" in data["detail"]


@pytest.mark.asyncio
async def test_change_password_missing_fields(test_client: TestClient, test_user: User):
    """Test changing password without required fields"""
    # First login to get token
    login_response = test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    access_token = login_data["access_token"]
    
    # Try to change password without required fields
    change_data = {
        "current_password": "password123"
        # Missing new_password
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/auth/change-password", json=change_data, headers=headers)
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_auth_endpoints_without_auth(test_client: TestClient):
    """Test that protected endpoints return 401 without authentication"""
    # Test /auth/me endpoint without auth
    response = test_client.get("/auth/me")
    assert response.status_code == 403  # Should be 403 due to security middleware
    
    # Test /auth/verify endpoint without auth
    response = test_client.get("/auth/verify")
    assert response.status_code == 403  # Should be 403 due to security middleware


@pytest.mark.asyncio
async def test_auth_endpoints_invalid_auth(test_client: TestClient):
    """Test that protected endpoints return 401 with invalid authentication"""
    headers = {"Authorization": "Bearer invalid_token"}
    
    # Test /auth/me endpoint with invalid auth
    response = test_client.get("/auth/me", headers=headers)
    assert response.status_code == 401
    
    # Test /auth/verify endpoint with invalid auth
    response = test_client.get("/auth/verify", headers=headers)
    assert response.status_code == 401