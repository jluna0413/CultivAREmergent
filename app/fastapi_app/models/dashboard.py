"""
Dashboard Models
Pydantic models for dashboard statistics and data.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CountStats(BaseModel):
    """Plant count statistics."""
    total: int = Field(..., description="Total number of plants")
    active: int = Field(..., description="Number of active plants")
    harvested: int = Field(..., description="Number of harvested plants")
    seedlings: int = Field(..., description="Number of seedlings")
    vegetative: int = Field(..., description="Number of vegetative plants")
    flowering: int = Field(..., description="Number of flowering plants")


class CultivarStats(BaseModel):
    """Cultivar statistics."""
    total_cultivars: int = Field(..., description="Total number of unique cultivars")
    user_cultivars: int = Field(..., description="Number of user's unique cultivars")


class EnvironmentalStats(BaseModel):
    """Environmental data statistics."""
    avg_temperature: float = Field(..., description="Average temperature")
    avg_humidity: float = Field(..., description="Average humidity")
    avg_ph: Optional[float] = Field(None, description="Average pH")
    avg_ec: Optional[float] = Field(None, description="Average EC")


class SensorStats(BaseModel):
    """Sensor statistics."""
    total_sensors: int = Field(..., description="Total number of sensors")
    active_sensors: int = Field(..., description="Number of active sensors")
    last_reading_time: Optional[datetime] = Field(None, description="Time of last sensor reading")


class DataSlice(BaseModel):
    """Data slice for chart visualization."""
    timestamp: datetime
    value: float
    label: Optional[str] = Field(None, description="Optional label for the data point")


class EnvironmentalSlice(BaseModel):
    """Environmental data slice for charts."""
    temperature_data: List[DataSlice] = Field(default_factory=list, description="Temperature trend data")
    humidity_data: List[DataSlice] = Field(default_factory=list, description="Humidity trend data")
    ph_data: List[DataSlice] = Field(default_factory=list, description="pH trend data")
    ec_data: List[DataSlice] = Field(default_factory=list, description="EC trend data")


class GrowthPhaseSlice(BaseModel):
    """Growth phase distribution data."""
    phase: str
    count: int
    percentage: float


class RecentReading(BaseModel):
    """Recent sensor readings."""
    timestamp: datetime
    sensor_type: str
    value: float
    unit: str
    location: Optional[str] = Field(None, description="Sensor location")


class RecentActivity(BaseModel):
    """Recent dashboard activities."""
    timestamp: datetime
    activity_type: str
    description: str
    plant_id: Optional[int] = Field(None, description="Related plant ID")
    severity: str = Field(..., description="Activity severity: info, warning, critical")


class DashboardStats(BaseModel):
    """
    Complete dashboard statistics response.
    
    This model provides all the statistical data needed to populate
    the Flutter dashboard screen with real-time information.
    """
    
    # Summary counts
    counts: CountStats = Field(..., description="Plant count statistics")
    
    # Cultivar information
    cultivars: CultivarStats = Field(..., description="Cultivar statistics")
    
    # Environmental data
    environment: EnvironmentalStats = Field(..., description="Environmental statistics")
    
    # Sensor data
    sensors: SensorStats = Field(..., description="Sensor statistics")
    
    # Chart data slices
    data_slices: EnvironmentalSlice = Field(..., description="Environmental trend data for charts")
    
    # Growth phase distribution
    growth_phases: List[GrowthPhaseSlice] = Field(
        default_factory=list, 
        description="Distribution of plants across growth phases"
    )
    
    # Recent readings
    recent_readings: List[RecentReading] = Field(
        default_factory=list,
        description="Most recent sensor readings"
    )
    
    # Recent activities
    recent_activities: List[RecentActivity] = Field(
        default_factory=list,
        description="Recent dashboard activities"
    )
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="When this data was generated")
    user_id: int = Field(..., description="User ID for which this data was generated")


class DashboardStatsRequest(BaseModel):
    """Request model for dashboard stats with optional parameters."""
    include_history: bool = Field(default=True, description="Include historical data for charts")
    time_range_hours: int = Field(default=24, description="Time range for historical data in hours")
    limit_recent_readings: int = Field(default=10, description="Limit number of recent readings")
    limit_recent_activities: int = Field(default=10, description="Limit number of recent activities")
