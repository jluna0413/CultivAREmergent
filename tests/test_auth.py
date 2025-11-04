"""
Test module for authentication endpoints.
Tests login, refresh, logout, and token validation endpoints.
"""

import pytest
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.fastapi_app.jwt_utils import create_access_token_with_jti, create_refresh_token_with_jti

# Import the app and models
from app.fastapi_app import app
from app.models_async.auth import User
from app.models_async.base import Base, get_async_session
from app.fastapi_app.routers.auth import router


def test_auth_router_import():
    """Test that the auth router can be imported"""
    from app.fastapi_app.routers import auth
    assert auth is not None
    assert hasattr(auth, 'router')


def test_login_request_model():
    """Test the LoginRequest Pydantic model"""
    from app.fastapi_app.routers.auth import LoginRequest
    
    # Valid data
    login_data = LoginRequest(username="testuser", password="password123")
    assert login_data.username == "testuser"
    assert login_data.password == "password123"
    
    # Test validation - empty username
    with pytest.raises(ValueError):
        LoginRequest(username="", password="password123")
    
    # Test validation - empty password
    with pytest.raises(ValueError):
        LoginRequest(username="testuser", password="")


def test_token_response_model():
    """Test the TokenResponse Pydantic model"""
    from app.fastapi_app.routers.auth import TokenResponse
    
    token_data = TokenResponse(
        access_token="access_token_string",
        refresh_token="refresh_token_string",
        expires_in=1800
    )
    
    assert token_data.access_token == "access_token_string"
    assert token_data.refresh_token == "refresh_token_string"
    assert token_data.token_type == "bearer"
    assert token_data.expires_in == 1800


def test_refresh_token_request_model():
    """Test the RefreshTokenRequest Pydantic model"""
    from app.fastapi_app.routers.auth import RefreshTokenRequest
    
    refresh_data = RefreshTokenRequest(refresh_token="refresh_token_string")
    assert refresh_data.refresh_token == "refresh_token_string"


def test_logout_request_model():
    """Test the LogoutRequest Pydantic model"""
    from app.fastapi_app.routers.auth import LogoutRequest
    
    logout_data = LogoutRequest(refresh_token="refresh_token_string")
    assert logout_data.refresh_token == "refresh_token_string"
    
    # Test with None value
    logout_data_none = LogoutRequest(refresh_token=None)
    assert logout_data_none.refresh_token is None


def test_user_response_model():
    """Test the UserResponse Pydantic model"""
    from app.fastapi_app.routers.auth import UserResponse
    
    # Create a mock user object
    user_data = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "is_admin": False,
        "user_type": "Grower",
        "created_at": datetime.now()
    }
    
    user_response = UserResponse(**user_data)
    assert user_response.id == 1
    assert user_response.username == "testuser"
    assert user_response.email == "test@example.com"
    assert user_response.is_admin is False
    assert user_response.user_type == "Grower"


class MockAsyncSession:
    """Mock async session for testing"""
    async def execute(self, query):
        # Mock execute method
        result = MagicMock()
        result.scalar_one_or_none = MagicMock()
        result.scalars = MagicMock()
        result.scalars.all = MagicMock(return_value=[])
        return result


@pytest.mark.asyncio
async def test_login_success():
    """Test successful login"""
    from app.fastapi_app.routers.auth import login
    from app.fastapi_app.routers.auth import LoginRequest
    
    # Create mock database session
    mock_db = MockAsyncSession()
    
    # Create a mock user object that has the required methods
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = "testuser" 
    mock_user.is_admin = False
    mock_user.force_password_change = False
    mock_user.check_password = MagicMock(return_value=True)
    
    # Mock the execute result
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_db.execute.return_value = mock_result
    
    login_data = LoginRequest(username="testuser", password="password123")
    
    # Call the login function
    response = await login(login_data, mock_db)
    
    # Verify the response
    assert hasattr(response, 'access_token')
    assert hasattr(response, 'refresh_token')
    assert response.token_type == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    from app.fastapi_app.routers.auth import login
    from app.fastapi_app.routers.auth import LoginRequest
    
    # Create mock database session
    mock_db = MockAsyncSession()
    
    # Mock the execute result to return None (no user found)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result
    
    login_data = LoginRequest(username="nonexistent", password="password123")
    
    # Expect HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        await login(login_data, mock_db)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_refresh_token_success():
    """Test successful token refresh"""
    from app.fastapi_app.routers.auth import refresh_token
    from app.fastapi_app.routers.auth import RefreshTokenRequest
    
    # Create mock database session
    mock_db = MockAsyncSession()
    
    # Create a mock user object
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.is_admin = False
    mock_user.force_password_change = False
    
    # Mock the execute result
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_db.execute.return_value = mock_result
    
    # Create a valid refresh token for testing
    user_data = {"user_id": 1, "username": "testuser", "is_admin": False}
    valid_refresh_token = create_refresh_token_with_jti(user_data)
    
    refresh_data = RefreshTokenRequest(refresh_token=valid_refresh_token)
    
    # Call the refresh_token function
    response = await refresh_token(refresh_data, mock_db)
    
    # Verify the response
    assert hasattr(response, 'access_token')
    assert hasattr(response, 'refresh_token')
    assert response.token_type == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_invalid():
    """Test refresh token with invalid token"""
    from app.fastapi_app.routers.auth import refresh_token
    from app.fastapi_app.routers.auth import RefreshTokenRequest
    
    # Create mock database session
    mock_db = MockAsyncSession()
    
    refresh_data = RefreshTokenRequest(refresh_token="invalid_token")
    
    # Expect HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        await refresh_token(refresh_data, mock_db)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_logout_success():
    """Test successful logout"""
    from app.fastapi_app.routers.auth import logout
    from app.fastapi_app.routers.auth import LogoutRequest
    
    # Create mock database session
    mock_db = MockAsyncSession()
    
    logout_data = LogoutRequest(refresh_token=None)
    
    # Call the logout function
    result = await logout(logout_data, None, mock_db)
    
    assert result == {"message": "Logout successful"}


def test_auth_router_mounted():
    """Test that auth router is properly mounted in the main app"""
    # Check if the auth routes exist in the app
    routes = [route.path for route in app.routes]
    
    expected_routes = [
        "/auth/login",
        "/auth/refresh", 
        "/auth/logout",
        "/auth/me",
        "/auth/verify",
        "/auth/change-password"
    ]
    
    for route in expected_routes:
        assert route in routes, f"Route {route} not found in app"