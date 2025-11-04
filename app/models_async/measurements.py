"""
Measurement models for tracking plant measurements (async version).
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from app.models_async.base import Base


class Measurement(Base):
    """Plant measurement model."""

    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plant.id", ondelete="CASCADE"), nullable=False)
    metric_id = Column(Integer, ForeignKey("metric.id"), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    # Relationships
    plant = relationship("Plant", back_populates="measurements")
    metric = relationship("Metric", back_populates="measurements")

    def __repr__(self) -> str:
        return f"<Measurement(id={self.id}, plant_id={self.plant_id}, metric_id={self.metric_id}, value={self.value})>"

    @property
    def metric_name(self) -> Optional[str]:
        return self.metric.name if self.metric else None

    @property
    def unit(self) -> Optional[str]:
        return self.metric.unit if self.metric else None