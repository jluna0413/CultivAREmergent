"""
Asynchronous database models for sensor-related data.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    func,
)
from .base import Base
from sqlalchemy.orm import relationship

# Assuming Zone is in grow.py, and IoT models will be in iot.py
# from .grow import Zone
# from .iot import ACInfinityDevice, EcowittDevice

class Sensor(Base):
    """Asynchronous Sensor model."""
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    source = Column(String(50)) # Stores string value of SensorSource Enum
    device = Column(String(100))
    sensor_type = Column(String(50)) # Renamed from 'type', stores string value of SensorType Enum
    show = Column(Boolean, default=True)
    unit = Column(String(20))
    location = Column(String(100)) # Added location
    ac_infinity_device_id = Column(Integer, ForeignKey("ac_infinity_devices.id"))
    ecowitt_device_id = Column(Integer, ForeignKey("ecowitt_devices.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    zone = relationship("Zone", backref="sensors")
    data = relationship("SensorData", back_populates="sensor", cascade="all, delete-orphan")
    ac_infinity_device = relationship("ACInfinityDevice", back_populates="sensors")
    ecowitt_device = relationship("EcowittDevice", back_populates="sensors")

    @property
    def zone_name(self):
        return self.zone.name if self.zone else None


class SensorData(Base):
    """Asynchronous Sensor Data model."""
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    sensor_type = Column(String(50))
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now()) # Renamed from timestamp
    
    sensor = relationship("Sensor", back_populates="data")

    @property
    def sensor_name(self):
        return self.sensor.name if self.sensor else None
