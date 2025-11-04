"""
Plant image models for tracking plant photos (async version).
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.models_async.base import Base


class PlantImage(Base):
    """Plant image model."""

    __tablename__ = "plant_image"

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plant.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String(255), nullable=False)
    image_description = Column(Text)
    image_order = Column(Integer, default=0)
    image_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plant = relationship("Plant", back_populates="images")

    def __repr__(self) -> str:
        return f"<PlantImage(id={self.id}, plant_id={self.plant_id}, image_path='{self.image_path}')>"

    @property
    def plant_name(self) -> Optional[str]:
        return self.plant.name if self.plant else None