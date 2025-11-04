"""
Async Sensor Models
Sensor device management and sensor readings for IoT integration.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models_async.base import Base


class Sensor(Base):
    """Sensor device model for tracking IoT sensors."""
    
    __tablename__ = "sensor"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Device Info
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    zone_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("zone.id"), nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    device: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sensor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Configuration
    show: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Device Integration
    ac_infinity_device_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ecowitt_device_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    zone = relationship("Zone", back_populates="sensors", foreign_keys=[zone_id])
    readings = relationship("SensorData", back_populates="sensor", cascade="all, delete-orphan")
    
    def to_dict(self) -> dict:
        """Convert sensor to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "zone_id": self.zone_id,
            "zone_name": self.zone.name if self.zone else None,
            "source": self.source,
            "device": self.device,
            "sensor_type": self.sensor_type,
            "show": self.show,
            "unit": self.unit,
            "ac_infinity_device_id": self.ac_infinity_device_id,
            "ecowitt_device_id": self.ecowitt_device_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "readings_count": len(self.readings) if self.readings else 0,
        }
    
    def __repr__(self) -> str:
        return f"<Sensor(id={self.id}, name='{self.name}', type='{self.sensor_type}')>"


class SensorData(Base):
    """Sensor reading model (temperature, humidity, etc)."""
    
    __tablename__ = "sensor_data"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Foreign Key
    sensor_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor.id"), nullable=False, index=True)
    
    # Reading
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    
    # Relationships
    sensor = relationship("Sensor", back_populates="readings")
    
    def to_dict(self) -> dict:
        """Convert sensor data to dictionary."""
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "sensor_name": self.sensor.name if self.sensor else None,
            "value": self.value,
            "unit": self.unit,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self) -> str:
        return f"<SensorData(id={self.id}, sensor_id={self.sensor_id}, value={self.value})>"


class Stream(Base):
    """Video stream model for time-lapse creation."""
    
    __tablename__ = "stream"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Stream Info
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Settings
    visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def to_dict(self) -> dict:
        """Convert stream to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "visible": self.visible,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self) -> str:
        return f"<Stream(id={self.id}, name='{self.name}', visible={self.visible})>"
