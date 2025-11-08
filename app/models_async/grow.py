"""
Async Grow Models
Plant, Cultivar, Breeder, Status, Grow, Metric, Zone models.
"""
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Index, func, JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models_async.base import Base

if TYPE_CHECKING:
    from app.models_async.auth import User
    from app.models_async.activities import PlantActivity
    from app.models_async.sensors import Sensor
    from app.models_async.measurements import Measurement
    from app.models_async.plant_images import PlantImage


class Breeder(Base):
    """Cannabis breeder model."""
    
    __tablename__ = "breeder"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # SeedFinder specific fields
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    seedfinder_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Case-insensitive unique index and new index for seedfinder_id
    __table_args__ = (
        Index('ux_breeder_name_lower', func.lower(name), unique=True),
        Index('ix_breeder_seedfinder_id', 'seedfinder_id', unique=True),
    )
    
    # Relationships
    cultivars: Mapped[List["Cultivar"]] = relationship("Cultivar", back_populates="breeder", lazy="selectin")
    
    def __repr__(self) -> str:
        country_info = f", country='{self.country}'" if self.country else ""
        return f"<Breeder(id={self.id}, name='{self.name}'{country_info})>"


class Cultivar(Base):
    """Cannabis cultivar/strain model."""
    
    __tablename__ = "cultivar"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    breeder_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("breeder.id"), nullable=True)
    
    # Genetics
    indica: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sativa: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    autoflower: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Lineage and Cannabinoid fields
    parent_1: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    parent_2: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    lineage_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    seedfinder_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    thc_content: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    cbd_content: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    flowering_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # photoperiod, autoflower, etc
    
    # Details
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    short_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    seed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cycle_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    __table_args__ = (
        Index('ix_cultivar_seedfinder_id', 'seedfinder_id', unique=True),
        Index('ix_cultivar_parent_1', 'parent_1'),
        Index('ix_cultivar_parent_2', 'parent_2'),
    )
    
    # Relationships
    breeder: Mapped[Optional["Breeder"]] = relationship("Breeder", back_populates="cultivars", lazy="selectin")
    plants: Mapped[List["Plant"]] = relationship("Plant", back_populates="cultivar")
    
    @property
    def breeder_name(self) -> Optional[str]:
        """Get breeder name if exists."""
        return self.breeder.name if self.breeder else None
    
    def __repr__(self) -> str:
        parents_info = ""
        if self.parent_1 and self.parent_2:
            parents_info = f", parents='{self.parent_1} x {self.parent_2}'"
        elif self.parent_1:
            parents_info = f", parent_1='{self.parent_1}'"
        return f"<Cultivar(id={self.id}, name='{self.name}'{parents_info})>"


class Status(Base):
    """Plant status model (Seedling, Vegetative, Flowering, etc)."""
    
    __tablename__ = "status"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Optional status history tracking
    plant_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("plant.id"), nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    plants: Mapped[List["Plant"]] = relationship("Plant", foreign_keys="Plant.status_id", back_populates="status")
    
    def __repr__(self) -> str:
        return f"<Status(id={self.id}, status='{self.status}')>"


class Zone(Base):
    """Growing zone/location model (Indoor, Outdoor, Tent, etc)."""
    
    __tablename__ = "zone"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    plants: Mapped[List["Plant"]] = relationship("Plant", back_populates="zone")
    sensors: Mapped[List["Sensor"]] = relationship("Sensor", back_populates="zone", foreign_keys="Sensor.zone_id")
    
    def __repr__(self) -> str:
        return f"<Zone(id={self.id}, name='{self.name}')>"


class Metric(Base):
    """Measurement metric model (height, pH, EC, etc)."""
    
    __tablename__ = "metric"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Relationships
    measurements: Mapped[List["Measurement"]] = relationship("Measurement", back_populates="metric")
    
    def __repr__(self) -> str:
        return f"<Metric(id={self.id}, name='{self.name}')>"


class Grow(Base):
    """Grow cycle model (represents a batch of plants)."""
    
    __tablename__ = "grow"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), default='active', nullable=False)
    
    # Dates
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Details
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="grows", lazy="selectin")
    plants: Mapped[List["Plant"]] = relationship("Plant", back_populates="grow", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Grow(id={self.id}, name='{self.name}', status='{self.status}')>"


class Plant(Base):
    """Plant model (individual cannabis plant)."""
    
    __tablename__ = "plant"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Basic Info
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign Keys
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey("status.id"), nullable=False)
    cultivar_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("cultivar.id"), nullable=True)
    zone_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("zone.id"), nullable=True)
    grow_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("grow.id"), nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("plant.id"), nullable=True)
    
    # Growth Tracking
    current_day: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_week: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_height: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Dates
    start_dt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    height_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_water_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_feed_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    harvest_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    est_harvest_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Growth Stage Dates
    germination_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    seedling_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    vegetative_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    flowering_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    curing_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Harvest Info
    harvest_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    cycle_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Flags
    is_clone: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    autoflower: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # External Links
    cultivar_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="plants", lazy="selectin")
    status: Mapped["Status"] = relationship("Status", foreign_keys=[status_id], back_populates="plants", lazy="selectin")
    cultivar: Mapped[Optional["Cultivar"]] = relationship("Cultivar", back_populates="plants", lazy="selectin")
    zone: Mapped[Optional["Zone"]] = relationship("Zone", back_populates="plants", lazy="selectin")
    grow: Mapped[Optional["Grow"]] = relationship("Grow", back_populates="plants", lazy="selectin")
    parent: Mapped[Optional["Plant"]] = relationship("Plant", remote_side=[id], foreign_keys=[parent_id])
    children: Mapped[List["Plant"]] = relationship("Plant", foreign_keys=[parent_id])
    activities: Mapped[List["PlantActivity"]] = relationship(
        "PlantActivity",
        back_populates="plant",
        cascade="all, delete-orphan"
    )
    measurements: Mapped[List["Measurement"]] = relationship(
        "Measurement",
        back_populates="plant",
        cascade="all, delete-orphan"
    )
    images: Mapped[List["PlantImage"]] = relationship(
        "PlantImage",
        back_populates="plant",
        cascade="all, delete-orphan"
    )
    
    # Computed Properties
    @property
    def status_name(self) -> Optional[str]:
        """Get status name."""
        return self.status.status if self.status else None
    
    @property
    def cultivar_name(self) -> Optional[str]:
        """Get cultivar name."""
        return self.cultivar.name if self.cultivar else None
    
    @property
    def breeder_name(self) -> Optional[str]:
        """Get breeder name through cultivar."""
        return self.cultivar.breeder_name if self.cultivar else None
    
    @property
    def zone_name(self) -> Optional[str]:
        """Get zone name."""
        return self.zone.name if self.zone else None
    
    @property
    def parent_name(self) -> Optional[str]:
        """Get parent plant name."""
        return self.parent.name if self.parent else None
    
    @property
    def grow_name(self) -> Optional[str]:
        """Get grow name."""
        return self.grow.name if self.grow else None
    
    def to_dict(self) -> dict:
        """Convert plant to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status_id": self.status_id,
            "status_name": self.status_name,
            "cultivar_id": self.cultivar_id,
            "cultivar_name": self.cultivar_name,
            "breeder_name": self.breeder_name,
            "zone_id": self.zone_id,
            "zone_name": self.zone_name,
            "grow_id": self.grow_id,
            "grow_name": self.grow_name,
            "current_day": self.current_day,
            "current_week": self.current_week,
            "current_height": self.current_height,
            "is_clone": self.is_clone,
            "autoflower": self.autoflower,
            "start_dt": self.start_dt.isoformat() if self.start_dt else None,
            "harvest_date": self.harvest_date.isoformat() if self.harvest_date else None,
            "harvest_weight": self.harvest_weight,
        }
    
    def __repr__(self) -> str:
        return f"<Plant(id={self.id}, name='{self.name}', status='{self.status_name}')>"
