"""
Async Activities Models
Activity tracking models for system and plant activities.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models_async.base import Base

if TYPE_CHECKING:
    from app.models_async.auth import User
    from app.models_async.grow import Plant


class Activity(Base):
    """Activity model for tracking system and user activities."""
    
    __tablename__ = "activity"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Activity Details
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # login, plant_add, strain_edit, etc.
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # system, user, plant
    
    # User Information
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    
    # Entity Information
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # plant, strain, breeder, clone, etc.
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    entity_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Activity Data
    title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string with additional details
    
    # Metadata
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Status
    is_system_activity: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Timestamps
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", backref="activities")
    
    # Indexes
    __table_args__ = (
        Index('ix_activity_user_id', 'user_id'),
        Index('ix_activity_type', 'type'),
        Index('ix_activity_activity_type', 'activity_type'),
        Index('ix_activity_entity_type_id', 'entity_type', 'entity_id'),
        Index('ix_activity_timestamp', 'timestamp'),
        Index('ix_activity_is_active', 'is_active'),
    )
    
    @property
    def is_recent(self) -> bool:
        """Check if activity is recent (within last 24 hours)."""
        return (datetime.utcnow() - self.timestamp).total_seconds() < 86400
    
    @property
    def details_dict(self) -> Optional[dict]:
        """Parse details JSON string to dictionary."""
        if not self.details:
            return None
        try:
            import json
            return json.loads(self.details)
        except (json.JSONDecodeError, TypeError):
            return None
    
    def set_details(self, details_dict: dict) -> None:
        """Set details from dictionary to JSON string."""
        if details_dict:
            import json
            self.details = json.dumps(details_dict)
    
    def __repr__(self) -> str:
        return f"<Activity(id={self.id}, type='{self.type}', user_id={self.user_id})>"


class PlantActivity(Base):
    """Plant-specific activity model."""
    
    __tablename__ = "plant_activity"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Plant Information
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey('plant.id'), nullable=False, index=True)
    plant_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Activity Details
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # feeding, watering, pruning, harvest, etc.
    activity_name: Mapped[str] = mapped_column(String(100), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # User Information
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    
    # Metadata
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Timestamps
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    plant: Mapped["Plant"] = relationship("Plant", backref="activities")
    user: Mapped[Optional["User"]] = relationship("User", backref="plant_activities")
    
    # Indexes
    __table_args__ = (
        Index('ix_plant_activity_plant_id', 'plant_id'),
        Index('ix_plant_activity_activity_type', 'activity_type'),
        Index('ix_plant_activity_date', 'date'),
        Index('ix_plant_activity_user_id', 'user_id'),
    )
    
    @property
    def is_recent(self) -> bool:
        """Check if activity is recent (within last 7 days)."""
        return (datetime.utcnow() - self.date).total_seconds() < 604800
    
    def __repr__(self) -> str:
        return f"<PlantActivity(id={self.id}, plant_id={self.plant_id}, activity='{self.activity_name}')>"


class ActivitySummary(Base):
    """Activity summary model for analytics and reporting."""
    
    __tablename__ = "activity_summary"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Summary Details
    summary_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # daily, weekly, monthly
    date_key: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    
    # Activity Metrics
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unique_users: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Additional Metrics
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Indexes
    __table_args__ = (
        Index('ix_activity_summary_type_date', 'summary_type', 'date_key'),
        Index('ix_activity_summary_activity_type', 'activity_type'),
        Index('ix_activity_summary_entity', 'entity_type', 'entity_id'),
    )
    
    def __repr__(self) -> str:
        return f"<ActivitySummary(id={self.id}, type='{self.summary_type}', date='{self.date_key}')>"