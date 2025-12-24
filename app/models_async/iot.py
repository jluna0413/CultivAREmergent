"""
Asynchronous database models for IoT devices.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
)
from .base import Base
from sqlalchemy.orm import relationship

class ACInfinityDevice(Base):
    """Asynchronous AC Infinity device model."""
    __tablename__ = "ac_infinity_devices"

    id = Column(Integer, primary_key=True)
    device_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100))
    type = Column(String(50))
    status = Column(String(20))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    sensors = relationship("Sensor", back_populates="ac_infinity_device")


class ACInfinityToken(Base):
    """Asynchronous AC Infinity authentication token model."""
    __tablename__ = "ac_infinity_tokens"

    id = Column(Integer, primary_key=True)
    access_token = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class EcowittDevice(Base):
    """Asynchronous Ecowitt device model."""
    __tablename__ = "ecowitt_devices"

    id = Column(Integer, primary_key=True)
    device_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100))
    ip_address = Column(String(45)) # Increased size for IPv6
    mac_address = Column(String(17))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    sensors = relationship("Sensor", back_populates="ecowitt_device")
