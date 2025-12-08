"""
AC Infinity specific models for the CultivAR application.
STRENGTHENED: Enhanced security for IoT device integration
"""

import hashlib
import secrets
from datetime import datetime, timezone
from sqlalchemy.types import Uuid
import uuid

from app.database import db


class ACInfinityDevice(db.Model):
    """AC Infinity device model with enhanced security."""

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='inactive', index=True)
    
    # Security enhancements
    device_uuid = db.Column(Uuid, default=uuid.uuid4, unique=True, nullable=False)
    api_key_hash = db.Column(db.String(128), nullable=False)  # Hashed API key
    device_fingerprint = db.Column(db.String(256))  # Device fingerprint for authentication
    last_heartbeat = db.Column(db.DateTime)  # Last communication timestamp
    connection_security_level = db.Column(db.String(20), default='basic', nullable=False)
    
    # Security settings
    requires_encryption = db.Column(db.Boolean, default=True, nullable=False)
    allowed_ip_ranges = db.Column(db.Text)  # Comma-separated IP ranges
    rate_limit_per_minute = db.Column(db.Integer, default=60)  # API calls per minute
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Security audit fields
    last_security_check = db.Column(db.DateTime)
    security_violations = db.Column(db.Integer, default=0)
    is_blocked = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    sensors = db.relationship("Sensor", backref="ac_infinity_device", lazy=True)

    def __init__(self, **kwargs):
        """Initialize AC Infinity device with security enhancements."""
        super().__init__(**kwargs)
        if not self.api_key_hash:
            self.api_key_hash = self._generate_api_key_hash()
        if not self.device_fingerprint:
            self.device_fingerprint = self._generate_device_fingerprint()

    def _generate_api_key_hash(self) -> str:
        """Generate secure API key hash for device authentication."""
        api_key = secrets.token_urlsafe(32)
        return hashlib.sha256(api_key.encode()).hexdigest()

    def _generate_device_fingerprint(self) -> str:
        """Generate unique device fingerprint for authentication."""
        unique_string = f"{self.device_id}{secrets.token_hex(16)}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    def verify_api_key(self, api_key: str) -> bool:
        """Verify API key for device authentication."""
        return self.api_key_hash == hashlib.sha256(api_key.encode()).hexdigest()

    def update_heartbeat(self) -> None:
        """Update device heartbeat timestamp."""
        self.last_heartbeat = datetime.now(timezone.utc)

    def is_connection_secure(self) -> bool:
        """Check if device connection meets security requirements."""
        return (self.connection_security_level in ['secure', 'high'] and
                self.requires_encryption and
                not self.is_blocked)

    def increment_security_violation(self) -> None:
        """Increment security violation counter."""
        self.security_violations += 1
        if self.security_violations >= 5:  # Block after 5 violations
            self.is_blocked = True


class ACInfinityToken(db.Model):
    """AC Infinity authentication token model with encryption."""

    id = db.Column(db.Integer, primary_key=True)
    access_token_hash = db.Column(db.String(128), nullable=False)  # Hashed token
    refresh_token_hash = db.Column(db.String(128), nullable=False)  # Hashed refresh token
    token_salt = db.Column(db.String(32), nullable=False)  # Salt for token hashing
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    
    # Security enhancements
    token_scope = db.Column(db.String(100))  # Token scope/permissions
    is_revoked = db.Column(db.Boolean, default=False, nullable=False, index=True)
    ip_restriction = db.Column(db.String(45))  # IPv4 or IPv6 address
    user_agent_hash = db.Column(db.String(64))  # User agent fingerprint
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_used = db.Column(db.DateTime)  # Last time token was used
    
    def __init__(self, access_token: str, refresh_token: str, **kwargs):
        """Initialize token with secure hashing."""
        super().__init__(**kwargs)
        self.token_salt = secrets.token_hex(16)
        self.access_token_hash = self._hash_token(access_token)
        self.refresh_token_hash = self._hash_token(refresh_token)

    def _hash_token(self, token: str) -> str:
        """Hash token with salt for secure storage."""
        return hashlib.sha256(f"{token}{self.token_salt}".encode()).hexdigest()

    def verify_access_token(self, token: str) -> bool:
        """Verify access token."""
        return (not self.is_revoked and
                self.access_token_hash == self._hash_token(token) and
                datetime.now(timezone.utc) < self.expires_at)

    def revoke_token(self) -> None:
        """Revoke the token."""
        self.is_revoked = True

    def update_last_used(self) -> None:
        """Update last used timestamp."""
        self.last_used = datetime.now(timezone.utc)
