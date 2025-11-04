"""
System-wide async models for the CultivAR application.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models_async.base import Base


class SystemActivity(Base):
    """System activity model for tracking system-wide activities."""

    __tablename__ = "system_activity"

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)  # login, plant_add, strain_edit, etc.
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    details = Column(Text)  # JSON string with activity details
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="system_activities")

    def __init__(self, user_id: Optional[int] = None, type: Optional[str] = None, 
                 details: Optional[str] = None, timestamp: Optional[datetime] = None):
        self.user_id = user_id
        self.type = type
        self.details = details
        self.timestamp = timestamp or datetime.utcnow()

    def __repr__(self):
        return f"<SystemActivity {self.type} by user {self.user_id} at {self.timestamp}>"