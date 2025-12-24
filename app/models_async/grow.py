"""
Asynchronous database models for grow-related data.
"""
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    Text,
    ForeignKey,
    func,
    JSON,
)
from .base import Base
from sqlalchemy.orm import relationship

# Assuming a User model exists in app.models_async.user
# from .user import User

class Cultivar(Base):
    """
    Asynchronous Cultivar (Strain) model.
    
    Comprehensive cannabis strain data including:
    - Basic info (name, breeder, genetics ratio)
    - Lineage and parentage
    - Cannabinoid profile (THC, CBD, CBG, THCV, CBC, CBN, etc.)
    - Terpene profile with individual terpene levels
    - Sensory profile (flavors, aromas)
    - Effects (recreational and medical)
    - Growing information
    """
    __tablename__ = "cultivars"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    breeder_id = Column(Integer, ForeignKey("breeders.id"))
    
    # Genetics Ratio
    indica = Column(Integer, default=0)  # Percentage
    sativa = Column(Integer, default=0)  # Percentage
    ruderalis = Column(Integer, default=0)  # Percentage (for autoflower lineage)
    autoflower = Column(Boolean, default=False)
    
    # Description & Marketing
    description = Column(Text)  # Full strain description
    short_description = Column(String(500))  # Brief tagline
    
    # Lineage & Parentage
    parent_1 = Column(String(100))  # Parent strain name
    parent_2 = Column(String(100))  # Parent strain name
    parent_1_id = Column(Integer, ForeignKey("cultivars.id"), nullable=True)
    parent_2_id = Column(Integer, ForeignKey("cultivars.id"), nullable=True)
    lineage_json = Column(JSON)  # Full lineage tree {"parents": [], "grandparents": [], ...}
    genetics_type = Column(String(50))  # "Hybrid", "Indica-Dominant", "Sativa-Dominant", "Pure Indica", "Pure Sativa"
    
    # External IDs
    seedfinder_id = Column(String(100))
    leafly_slug = Column(String(100))
    weedmaps_id = Column(String(100))
    
    # ─── Cannabinoid Profile ─────────────────────────────────────────────
    # Primary Cannabinoids (percentages)
    thc_content = Column(Float)  # THC %
    thc_min = Column(Float)  # THC range minimum
    thc_max = Column(Float)  # THC range maximum
    cbd_content = Column(Float)  # CBD %
    cbd_min = Column(Float)
    cbd_max = Column(Float)
    
    # Secondary Cannabinoids
    cbg_content = Column(Float)  # CBG % (Cannabigerol)
    thcv_content = Column(Float)  # THCV % (Tetrahydrocannabivarin)
    cbc_content = Column(Float)  # CBC % (Cannabichromene)
    cbn_content = Column(Float)  # CBN % (Cannabinol)
    delta8_content = Column(Float)  # Delta-8 THC %
    thca_content = Column(Float)  # THCA % (raw form)
    cbda_content = Column(Float)  # CBDA % (raw form)
    
    # Full cannabinoid profile as JSON for extensibility
    cannabinoid_profile = Column(JSON)  # {"thc": 22.5, "cbd": 0.5, "cbg": 0.8, ...}
    
    # ─── Terpene Profile ─────────────────────────────────────────────────
    # Individual dominant terpenes (percentages)
    myrcene = Column(Float)  # Earthy, musky, herbal
    limonene = Column(Float)  # Citrus, lemon
    caryophyllene = Column(Float)  # Spicy, peppery
    linalool = Column(Float)  # Floral, lavender
    pinene = Column(Float)  # Pine, forest
    humulene = Column(Float)  # Hoppy, earthy
    terpinolene = Column(Float)  # Floral, herbal, piney
    ocimene = Column(Float)  # Sweet, herbal, woody
    bisabolol = Column(Float)  # Floral, chamomile
    
    # Full terpene profile as JSON for extensibility
    terpene_profile = Column(JSON)  # {"myrcene": 0.45, "limonene": 0.32, ...}
    dominant_terpene = Column(String(50))  # Primary terpene
    
    # ─── Sensory Profile ─────────────────────────────────────────────────
    flavors = Column(JSON)  # ["Citrus", "Pine", "Earthy", "Sweet"]
    aromas = Column(JSON)  # ["Skunky", "Diesel", "Fruity"]
    taste_description = Column(Text)  # Detailed taste notes
    aroma_description = Column(Text)  # Detailed aroma notes
    
    # ─── Effects ─────────────────────────────────────────────────────────
    effects = Column(JSON)  # ["Relaxed", "Happy", "Euphoric", "Creative", "Focused"]
    effects_description = Column(Text)  # Narrative description of effects
    
    # Medical Benefits
    medical_benefits = Column(JSON)  # ["Pain", "Anxiety", "Insomnia", "Depression", "Nausea"]
    medical_description = Column(Text)  # Detailed medical use cases
    
    # Negative Effects / Side Effects
    negative_effects = Column(JSON)  # ["Dry Mouth", "Dry Eyes", "Paranoia", "Anxiety"]
    
    # Effect Intensity (1-10 scale)
    potency_rating = Column(Integer)  # Overall potency
    body_high = Column(Integer)  # Body effect intensity
    head_high = Column(Integer)  # Cerebral effect intensity
    
    # ─── Growing Information ─────────────────────────────────────────────
    flowering_type = Column(String(50))  # "Photoperiod", "Autoflower"
    flowering_time_min = Column(Integer)  # Days (minimum)
    flowering_time_max = Column(Integer)  # Days (maximum)
    cycle_time = Column(Integer)  # Total cycle days (seed to harvest)
    
    # Yield Information
    yield_indoor = Column(String(50))  # e.g., "400-500 g/m²"
    yield_outdoor = Column(String(50))  # e.g., "500-700 g/plant"
    
    # Plant Characteristics
    height_indoor = Column(String(50))  # e.g., "80-120 cm"
    height_outdoor = Column(String(50))  # e.g., "150-200 cm"
    grow_difficulty = Column(String(50))  # "Easy", "Moderate", "Difficult", "Expert"
    
    # Climate Preferences
    climate = Column(JSON)  # ["Mediterranean", "Continental", "Tropical"]
    optimal_temp_min = Column(Integer)  # Celsius
    optimal_temp_max = Column(Integer)  # Celsius
    humidity_preference = Column(String(50))  # "Low", "Medium", "High"
    
    # Resistance
    mold_resistance = Column(String(50))  # "Low", "Medium", "High"
    pest_resistance = Column(String(50))
    
    # ─── Inventory & URLs ────────────────────────────────────────────────
    seed_count = Column(Integer, default=0)  # User's seed inventory
    url = Column(String(255))  # Official strain page
    image_urls = Column(JSON, default=list)  # List of image URLs
    
    # ─── Metadata ────────────────────────────────────────────────────────
    data_source = Column(String(50))  # "seedfinder", "leafly", "user", "verified"
    last_verified = Column(DateTime)  # When data was last verified
    verification_status = Column(String(50))  # "verified", "pending", "unverified"
    
    # Awards and Recognition
    awards = Column(JSON)  # [{"name": "Cannabis Cup 2023", "category": "Best Indica"}]
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # ─── Relationships ───────────────────────────────────────────────────
    breeder = relationship("Breeder", back_populates="cultivars")
    plants = relationship("Plant", back_populates="cultivar")
    
    # Self-referencing lineage relationships
    parent1_ref = relationship("Cultivar", remote_side=[id], foreign_keys=[parent_1_id])
    parent2_ref = relationship("Cultivar", remote_side=[id], foreign_keys=[parent_2_id])



class Breeder(Base):
    """Asynchronous Breeder model."""
    __tablename__ = "breeders"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100))
    website = Column(String(255))
    seedfinder_id = Column(String(100))
    description = Column(Text)

    cultivars = relationship("Cultivar", back_populates="breeder")
    marketplace_profile = relationship("MarketplaceBreeder", back_populates="global_breeder", uselist=False, primaryjoin="Breeder.id == MarketplaceBreeder.breeder_id")


class Status(Base):
    """Asynchronous Plant Status model."""
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    status = Column(String(50), nullable=False)
    
    plants = relationship("Plant", back_populates="status")


class Plant(Base):
    """Asynchronous Plant model."""
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Added
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status_id = Column(Integer, ForeignKey("statuses.id"), nullable=False)
    cultivar_id = Column(Integer, ForeignKey("cultivars.id"))
    zone_id = Column(Integer, ForeignKey("zones.id"))
    current_day = Column(Integer, default=0)
    current_week = Column(Integer, default=0)
    current_height = Column(String(20))
    height_date = Column(DateTime)
    last_water_date = Column(DateTime)
    last_feed_date = Column(DateTime)
    is_clone = Column(Boolean, default=False)
    start_dt = Column(DateTime, default=func.now())
    harvest_weight = Column(Float)
    harvest_date = Column(DateTime)
    cycle_time = Column(Integer)
    strain_url = Column(String(255))
    est_harvest_date = Column(DateTime)
    autoflower = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey("plants.id"))
    image_url = Column(String(255)) # Added
    created_at = Column(DateTime, default=func.now()) # Added
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) # Added

    # Relationships
    user = relationship("User", back_populates="plants")
    cultivar = relationship("Cultivar", back_populates="plants")
    status = relationship("Status", back_populates="plants")
    zone = relationship("Zone", back_populates="plants")
    parent = relationship("Plant", remote_side=[id], back_populates="children")
    children = relationship("Plant", back_populates="parent", cascade="all, delete-orphan")
    plant_activities = relationship("PlantActivity", back_populates="plant", cascade="all, delete-orphan") # Updated to reference PlantActivity from activities.py
    measurements = relationship("Measurement", back_populates="plant", cascade="all, delete-orphan")
    images = relationship("PlantImage", back_populates="plant", cascade="all, delete-orphan", order_by="PlantImage.image_date.desc()")

    @property
    def status_name(self):
        return self.status.status if self.status else None

    @property
    def strain_name(self):
        return self.cultivar.name if self.cultivar else None

    @property
    def breeder_name(self):
        return self.cultivar.breeder.name if self.cultivar and self.cultivar.breeder else None

    @property
    def zone_name(self):
        return self.zone.name if self.zone else None

    @property
    def parent_name(self):
        return self.parent.name if self.parent else None
        
    @property
    def latest_image(self):
        return self.images[0] if self.images else None


class Zone(Base):
    """Asynchronous Zone model."""
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    plants = relationship("Plant", back_populates="zone")
    streams = relationship("Stream", back_populates="zone")


class PlantImage(Base):
    """Asynchronous Plant image model."""
    __tablename__ = "plant_images"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    image_path = Column(String(255), nullable=False)
    image_description = Column(Text)
    image_order = Column(Integer, default=0)
    image_date = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    plant = relationship("Plant", back_populates="images")


class Measurement(Base):
    """Asynchronous Plant measurement model."""
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    metric_id = Column(Integer, ForeignKey("metrics.id"), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=func.now())

    plant = relationship("Plant", back_populates="measurements")
    metric = relationship("Metric", back_populates="measurements")


class Metric(Base):
    """Asynchronous Measurement metric model."""
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)

    measurements = relationship("Measurement", back_populates="metric")


class Stream(Base):
    """Asynchronous Video stream model."""
    __tablename__ = "streams"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    visible = Column(Boolean, default=True)

    zone = relationship("Zone", back_populates="streams")

    @property
    def zone_name(self):
        return self.zone.name if self.zone else None


class Grow(Base):
    """Asynchronous Grow cycle model."""
    __tablename__ = "grows"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    description = Column(Text)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    status = Column(String(50), default="active")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships can be added later as needed
    # plants = relationship("Plant", back_populates="grow") # If linking plants to grows explicitly
