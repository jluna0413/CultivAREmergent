"""
Unified Authentication Service
Provides consistent authentication across Flask and FastAPI frameworks
"""

from jose import jwt, JWTError
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models_async.auth import User
from app.config.config import Config


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class TokenValidationError(Exception):
    """Raised when token validation fails"""
    pass


class UnifiedAuthService:
    """
    Unified authentication service that works across Flask and FastAPI.
    Provides JWT token generation, validation, and user authentication.
    """
    
    def __init__(self):
        """Initialize the authentication service"""
        self.jwt_secret = self._get_jwt_secret()
        self.jwt_algorithm = Config.JWT_ALGORITHM or 'HS256'
        self.jwt_expiration_minutes = Config.JWT_EXPIRATION_MINUTES or 1440  # 24 hours
    
    def _get_jwt_secret(self) -> str:
        """Get JWT secret from environment or raise error"""
        jwt_secret = Config.JWT_SECRET_KEY or Config.get_fastapi_secrets()['JWT_SECRET_KEY']
        if not jwt_secret:
            raise ValueError("JWT_SECRET_KEY must be configured for authentication")
        return jwt_secret
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False
    
    def generate_token(self, user: User, additional_claims: Dict[str, Any] = None) -> str:
        """
        Generate a JWT token for the given user.
        
        Args:
            user: User object
            additional_claims: Additional claims to include in token
            
        Returns:
            JWT token string
        """
        now = datetime.now(timezone.utc)
        
        payload = {
            'user_id': user.id,
            'username': getattr(user, 'username', None),
            'email': getattr(user, 'email', None),
            'is_admin': getattr(user, 'is_admin', False),
            'iat': now,
            'exp': now + timedelta(minutes=self.jwt_expiration_minutes),
        }
        
        # Add additional claims if provided
        if additional_claims:
            payload.update(additional_claims)
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token if isinstance(token, str) else token.decode('utf-8')
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate a JWT token and return the payload.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload dictionary
            
        Raises:
            TokenValidationError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token, 
                self.jwt_secret, 
                algorithms=[self.jwt_algorithm]
            )
            return payload
        except JWTError as e:
            if "expired" in str(e).lower():
                raise TokenValidationError("Token has expired")
            else:
                raise TokenValidationError(f"Invalid token: {str(e)}")
        except Exception as e:
            raise TokenValidationError(f"Token validation error: {str(e)}")
    
    async def authenticate_user(self, session: AsyncSession, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        
        Args:
            session: Async database session
            email: User email
            password: User password
            
        Returns:
            User object if authentication successful, None otherwise
            
        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            # Get user by email
            result = await session.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            # Verify password
            if not self.verify_password(password, user.password_hash):
                return None
            
            # Check if user is active
            if hasattr(user, 'is_active') and not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            raise AuthenticationError(f"Authentication error: {str(e)}")
    
    def create_user_session_data(self, user: User) -> Dict[str, Any]:
        """
        Create session data for user (Flask session format).
        
        Args:
            user: User object
            
        Returns:
            Session data dictionary
        """
        return {
            'user_id': user.id,
            'username': getattr(user, 'username', ''),
            'email': getattr(user, 'email', ''),
            'is_admin': getattr(user, 'is_admin', False),
            'login_time': datetime.now(timezone.utc).isoformat(),
        }
    
    def create_api_session_data(self, user: User) -> Dict[str, Any]:
        """
        Create session data for API (FastAPI format).
        
        Args:
            user: User object
            
        Returns:
            API session data dictionary
        """
        return {
            'sub': str(user.id),  # Subject claim for JWT
            'username': getattr(user, 'username', ''),
            'email': getattr(user, 'email', ''),
            'is_admin': getattr(user, 'is_admin', False),
        }
    
    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Extract user information from a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            User information dictionary or None if invalid
        """
        try:
            payload = self.validate_token(token)
            return {
                'user_id': payload.get('user_id'),
                'username': payload.get('username'),
                'email': payload.get('email'),
                'is_admin': payload.get('is_admin', False),
            }
        except TokenValidationError:
            return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """
        Refresh a JWT token if it's still valid.
        
        Args:
            token: Current JWT token
            
        Returns:
            New JWT token or None if refresh not possible
        """
        try:
            payload = self.validate_token(token)
            
            # Create new token with updated expiration
            user_data = {
                'user_id': payload.get('user_id'),
                'username': payload.get('username'),
                'email': payload.get('email'),
                'is_admin': payload.get('is_admin', False),
            }
            
            # Create a mock user object for token generation
            class MockUser:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)

            mock_user = MockUser(user_data)
            return self.generate_token(mock_user)
            
        except TokenValidationError:
            return None
    
    def logout_cleanup(self, token: str) -> bool:
        """
        Perform cleanup operations for logout.
        
        Args:
            token: JWT token to invalidate
            
        Returns:
            True if cleanup successful
        """
        try:
            # In a production system, you might want to:
            # 1. Add token to a blacklist
            # 2. Store in Redis with expiration
            # 3. Log the logout event
            
            # For now, just validate the token format
            self.validate_token(token)
            return True
            
        except TokenValidationError:
            # Token is already invalid, that's fine for logout
            return True
        except Exception:
            return False


# Global instance
auth_service = UnifiedAuthService()


# Convenience functions for easy importing
def authenticate_user(email: str, password: str, session: AsyncSession) -> Optional[User]:
    """Convenience function to authenticate a user"""
    return auth_service.authenticate_user(session, email, password)


def generate_jwt_token(user: User) -> str:
    """Convenience function to generate JWT token"""
    return auth_service.generate_token(user)


def validate_jwt_token(token: str) -> Dict[str, Any]:
    """Convenience function to validate JWT token"""
    return auth_service.validate_token(token)


def hash_password(password: str) -> str:
    """Convenience function to hash password"""
    return auth_service.hash_password(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Convenience function to verify password"""
    return auth_service.verify_password(password, hashed_password)