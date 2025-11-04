"""
Pydantic models for Sensors domain.
Sensor device management and sensor readings for IoT integration.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Union
from pydantic import BaseModel, Field, validator


class SensorType(str, Enum):
    """Enum for different sensor types."""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PH = "ph"
    EC = "ec"
    CO2 = "co2"
    LIGHT = "light"
    SOIL_MOISTURE = "soil_moisture"
    AIR_PRESSURE = "air_pressure"
    WIND_SPEED = "wind_speed"
    RAIN = "rain"
    UV = "uv"
    WATER_LEVEL = "water_level"
    FLOW_RATE = "flow_rate"
    POWER = "power"
    OTHER = "other"


class SensorSource(str, Enum):
    """Enum for sensor data sources."""
    AC_INFINITY = "ac_infinity"
    ECOWITT = "ecowitt"
    MANUAL = "manual"
    API = "api"
    UNKNOWN = "unknown"


class SensorBase(BaseModel):
    """Base sensor model with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Sensor name")
    zone_id: Optional[int] = Field(None, description="Zone ID")
    source: Optional[SensorSource] = Field(None, description="Data source")
    device: Optional[str] = Field(None, max_length=100, description="Device name")
    sensor_type: SensorType = Field(..., description="Type of sensor")
    show: bool = Field(True, description="Whether to display sensor")
    unit: Optional[str] = Field(None, max_length=20, description="Measurement unit")
    ac_infinity_device_id: Optional[int] = Field(None, description="AC Infinity device ID")
    ecowitt_device_id: Optional[int] = Field(None, description="Ecowitt device ID")


class SensorCreate(SensorBase):
    """Model for creating a new sensor."""
    pass


class SensorUpdate(BaseModel):
    """Model for updating an existing sensor."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    zone_id: Optional[int] = None
    source: Optional[SensorSource] = None
    device: Optional[str] = Field(None, max_length=100)
    sensor_type: Optional[SensorType] = None
    show: Optional[bool] = None
    unit: Optional[str] = Field(None, max_length=20)
    ac_infinity_device_id: Optional[int] = None
    ecowitt_device_id: Optional[int] = None


class SensorResponse(SensorBase):
    """Model for sensor response with computed fields."""
    id: int = Field(..., description="Sensor ID")
    zone_name: Optional[str] = Field(None, description="Zone name")
    readings_count: int = Field(0, description="Number of readings")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    latest_reading: Optional["SensorReading"] = Field(None, description="Latest sensor reading")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class SensorListResponse(BaseModel):
    """Model for paginated sensor list response."""
    items: List[SensorResponse] = Field(..., description="List of sensors")
    total: int = Field(..., description="Total number of sensors")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class SensorFilters(BaseModel):
    """Model for sensor filtering parameters."""
    zone_id: Optional[int] = None
    sensor_type: Optional[SensorType] = None
    source: Optional[SensorSource] = None
    show: Optional[bool] = None
    search: Optional[str] = Field(None, description="Search term for name/device")


class SensorReading(BaseModel):
    """Model for individual sensor reading."""
    id: int = Field(..., description="Reading ID")
    sensor_id: int = Field(..., description="Sensor ID")
    sensor_name: Optional[str] = Field(None, description="Sensor name")
    value: float = Field(..., description="Sensor reading value")
    unit: Optional[str] = Field(None, description="Measurement unit")
    created_at: datetime = Field(..., description="Reading timestamp")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class SensorReadingCreate(BaseModel):
    """Model for creating a new sensor reading."""
    value: float = Field(..., description="Sensor reading value")
    unit: Optional[str] = Field(None, max_length=20, description="Measurement unit")


class SensorReadingResponse(BaseModel):
    """Model for sensor reading response."""
    reading: SensorReading = Field(..., description="Sensor reading data")
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


class SensorReadingsListResponse(BaseModel):
    """Model for paginated sensor readings list response."""
    items: List[SensorReading] = Field(..., description="List of sensor readings")
    total: int = Field(..., description="Total number of readings")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class SensorStats(BaseModel):
    """Model for sensor statistics."""
    total_sensors: int = Field(..., description="Total number of sensors")
    active_sensors: int = Field(..., description="Number of active sensors")
    sensors_by_type: dict[str, int] = Field(..., description="Sensors grouped by type")
    sensors_by_zone: dict[str, int] = Field(..., description="Sensors grouped by zone")
    sensors_by_source: dict[str, int] = Field(..., description="Sensors grouped by source")
    recent_readings_count: int = Field(..., description="Readings in last 24 hours")


class SensorStatsResponse(BaseModel):
    """Model for sensor statistics response."""
    stats: SensorStats = Field(..., description="Sensor statistics")
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


class SensorTypesResponse(BaseModel):
    """Model for available sensor types response."""
    sensor_types: List[SensorType] = Field(..., description="Available sensor types")
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


class SensorCreateResponse(BaseModel):
    """Model for sensor creation response."""
    sensor_id: int = Field(..., description="Created sensor ID")
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


class SensorUpdateResponse(BaseModel):
    """Model for sensor update response."""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


class SensorDeleteResponse(BaseModel):
    """Model for sensor deletion response."""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status")


# Response model for list API following newsletter pattern
class SensorListApiResponse(BaseModel):
    """Response model for sensor list API following established pattern."""
    items: List[SensorResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool


# Update forward references
SensorResponse.model_rebuild()
SensorReading.model_rebuild()