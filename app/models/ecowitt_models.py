"""
Ecowitt specific models for the CultivAR application.
STRENGTHENED: Enhanced security for IoT device integration
"""

import hashlib
import secrets
import ipaddress
from datetime import datetime, timezone
from sqlalchemy.types import Uuid
import uuid
import re

from app.database import db


class EcowittDevice(db.Model):
    """Ecowitt device model with enhanced security."""

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False, index=True)
    mac_address = db.Column(db.String(17), nullable=False)
    
    # Security enhancements
    device_uuid = db.Column(Uuid, default=uuid.uuid4, unique=True, nullable=False)
    api_key_hash = db.Column(db.String(128), nullable=False)  # Hashed API key
    device_fingerprint = db.Column(db.String(256))  # Device fingerprint for authentication
    last_heartbeat = db.Column(db.DateTime)  # Last communication timestamp
    connection_security_level = db.Column(db.String(20), default='basic', nullable=False)
    
    # Network security
    is_local_only = db.Column(db.Boolean, default=True, nullable=False)  # LAN-only access
    allowed_ip_ranges = db.Column(db.Text)  # Comma-separated IP ranges/CIDR
    requires_certificate = db.Column(db.Boolean, default=True, nullable=False)
    certificate_hash = db.Column(db.String(64))  # Device certificate fingerprint
    
    # Rate limiting and monitoring
    rate_limit_per_minute = db.Column(db.Integer, default=60)  # API calls per minute
    max_concurrent_connections = db.Column(db.Integer, default=5)
    connection_timeout_seconds = db.Column(db.Integer, default=30)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Security audit fields
    last_security_check = db.Column(db.DateTime)
    security_violations = db.Column(db.Integer, default=0)
    is_blocked = db.Column(db.Boolean, default=False, nullable=False)
    last_blocked_reason = db.Column(db.String(255))

    # Relationships
    sensors = db.relationship("Sensor", backref="ecowitt_device", lazy=True)

    def __init__(self, **kwargs):
        """Initialize Ecowitt device with security enhancements."""
        super().__init__(**kwargs)
        if not self.api_key_hash:
            self.api_key_hash = self._generate_api_key_hash()
        if not self.device_fingerprint:
            self.device_fingerprint = self._generate_device_fingerprint()
        if not self.certificate_hash:
            self.certificate_hash = self._generate_certificate_hash()

    def _generate_api_key_hash(self) -> str:
        """Generate secure API key hash for device authentication."""
        api_key = secrets.token_urlsafe(32)
        return hashlib.sha256(api_key.encode()).hexdigest()

    def _generate_device_fingerprint(self) -> str:
        """Generate unique device fingerprint for authentication."""
        unique_string = f"{self.device_id}{self.mac_address}{secrets.token_hex(16)}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    def _generate_certificate_hash(self) -> str:
        """Generate certificate hash for secure communication."""
        cert_data = f"{self.device_id}{secrets.token_hex(32)}"
        return hashlib.sha256(cert_data.encode()).hexdigest()

    def verify_api_key(self, api_key: str) -> bool:
        """Verify API key for device authentication."""
        return self.api_key_hash == hashlib.sha256(api_key.encode()).hexdigest()

    def validate_ip_access(self, client_ip: str) -> bool:
        """Validate if client IP is allowed to access device."""
        if self.is_blocked:
            return False
            
        # If no IP restrictions, allow all
        if not self.allowed_ip_ranges:
            return True
            
        try:
            client_ip_obj = ipaddress.ip_address(client_ip)
            allowed_ranges = self.allowed_ip_ranges.split(',')
            
            for allowed_range in allowed_ranges:
                allowed_range = allowed_range.strip()
                if '/' in allowed_range:
                    # CIDR notation
                    if client_ip_obj in ipaddress.ip_network(allowed_range, strict=False):
                        return True
                else:
                    # Single IP
                    if str(client_ip_obj) == allowed_range:
                        return True
            
            return False
        except (ValueError, ipaddress.AddressValueError):
            return False

    def update_heartbeat(self) -> None:
        """Update device heartbeat timestamp."""
        self.last_heartbeat = datetime.now(timezone.utc)

    def is_connection_secure(self) -> bool:
        """Check if device connection meets security requirements."""
        return (self.connection_security_level in ['secure', 'high'] and
                self.requires_certificate and
                not self.is_blocked)

    def increment_security_violation(self, reason: str = None) -> None:
        """Increment security violation counter."""
        self.security_violations += 1
        if reason:
            self.last_blocked_reason = reason
        if self.security_violations >= 3:  # Stricter limit for Ecowitt (LAN devices)
            self.is_blocked = True

    def validate_mac_address(self, mac_address: str) -> bool:
        """Validate MAC address format and security."""
        # Check MAC address format
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if not re.match(mac_pattern, mac_address):
            return False
        
        # Check if MAC address matches device
        normalized_mac = mac_address.lower().replace(':', '').replace('-', '')
        device_mac = self.mac_address.lower().replace(':', '').replace('-', '')
        
        return normalized_mac == device_mac

    def validate_ip_format(self, ip_address: str) -> bool:
        """Validate IP address format and security."""
        try:
            ip_obj = ipaddress.ip_address(ip_address)
            # Only allow IPv4 and IPv6 private ranges for security
            if ip_obj.is_private or ip_obj.is_loopback:
                return True
            # Allow link-local addresses
            if ip_obj.is_link_local:
                return True
            return False
        except (ValueError, ipaddress.AddressValueError):
            return False

    def is_device_online(self) -> bool:
        """Check if device is currently online based on heartbeat."""
        if not self.last_heartbeat:
            return False
        
        # Consider device offline if no heartbeat in last 10 minutes
        time_diff = datetime.now(timezone.utc) - self.last_heartbeat
        return time_diff.total_seconds() < 600  # 10 minutes

    def get_security_status(self) -> dict:
        """Get comprehensive security status of device."""
        return {
            'is_blocked': self.is_blocked,
            'security_violations': self.security_violations,
            'connection_secure': self.is_connection_secure(),
            'device_online': self.is_device_online(),
            'security_level': self.connection_security_level,
            'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            'last_blocked_reason': self.last_blocked_reason,
            'requires_certificate': self.requires_certificate,
            'is_local_only': self.is_local_only
        }
