"""
Asynchronous database models for activity-related data.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    func,
    Boolean,
    JSON # Import JSON type for details field
)
from sqlalchemy.orm import relationship
from .base import Base

# Assuming User model exists in app.models_async.auth
# from .auth import User # Not directly imported here, but referenced by relationship

class ActivityType(Base):
    """Asynchronous Activity Type model (e.g., 'login', 'plant_add')."""
    __tablename__ = "activity_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(50)) # e.g., 'system', 'user', 'plant'
    is_system = Column(Boolean, default=False)

    # Relationship to ActivityLog
    activity_logs = relationship("ActivityLog", back_populates="activity_type_rel")
    plant_activities = relationship("PlantActivity", back_populates="activity_type_rel")


class ActivityLog(Base):
    """Asynchronous Activity Log model for tracking all application activities."""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for system activities
    activity_type_id = Column(Integer, ForeignKey("activity_types.id"), nullable=False)
    
    # Fields from Pydantic ActivityBase
    type = Column(String(50), nullable=False) # e.g., 'login', 'plant_add'
    activity_category = Column(String(50), nullable=False) # e.g., 'system', 'user', 'plant'
    title = Column(String(255))
    description = Column(Text)
    entity_type = Column(String(50)) # e.g., 'plant', 'cultivar', 'breeder'
    entity_id = Column(Integer)
    entity_name = Column(String(255))
    username = Column(String(80)) # Denormalized for easier querying
    ip_address = Column(String(45)) # IPv4 or IPv6
    user_agent = Column(String(255))
    session_id = Column(String(255))
    details = Column(JSON) # Store additional details as JSON
    is_system_activity = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True) # For soft delete or archival

    timestamp = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="activity_logs")
    activity_type_rel = relationship("ActivityType", back_populates="activity_logs")


class PlantActivity(Base):
    """Asynchronous Plant Activity model."""
    __tablename__ = "plant_activities"

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    activity_type_id = Column(Integer, ForeignKey("activity_types.id"), nullable=False) # Renamed from activity_id
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Who performed the activity
    
    # Fields from Pydantic PlantActivityBase
    activity_name = Column(String(100), nullable=False) # e.g., 'feeding', 'watering'
    note = Column(Text)
    username = Column(String(80)) # Denormalized
    ip_address = Column(String(45))
    # details = Column(JSON) # Store structured activity data (Mismatch with legacy DB)

    date = Column(DateTime, default=func.now()) # Original date field
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    plant = relationship("Plant", back_populates="plant_activities")
    activity_type_rel = relationship("ActivityType", back_populates="plant_activities")
    user = relationship("User", back_populates="plant_activities")

# Add back_populates to User model in app.models_async.auth.py
# User.activity_logs = relationship("ActivityLog", back_populates="user")
# User.plant_activities = relationship("PlantActivity", back_populates="user")