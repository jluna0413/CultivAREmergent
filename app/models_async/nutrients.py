"""
Nutrient Management Models for CultivAR
Native integration of nutrient calculator functionality.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON, Date
from sqlalchemy.orm import relationship
from app.models_async.base import Base


class NutrientBrand(Base):
    """Nutrient brand/line (e.g., General Hydroponics, Fox Farm)."""
    __tablename__ = "nutrient_brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    manufacturer = Column(String(100))
    brand_type = Column(String(50), nullable=False)  # '3-part', '2-part', '1-part', 'organic'
    component_count = Column(Integer, nullable=False, default=1)
    description = Column(Text)
    website_url = Column(String(255))
   
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    components = relationship("NutrientComponent", back_populates="brand", cascade="all, delete-orphan")
    formulas = relationship("NutrientFormula", back_populates="brand", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<NutrientBrand {self.name}>"


class NutrientComponent(Base):
    """Individual nutrient component (e.g., FloraGro, FloraMicro, FloraBloom)."""
    __tablename__ = "nutrient_components"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("nutrient_brands.id"), nullable=False)
    name = Column(String(100), nullable=False)
    npk_ratio = Column(String(20))  # e.g., "3-0-0", "5-0-1"
    description = Column(Text)
    order_index = Column(Integer, default=0)  # Display order
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    brand = relationship("NutrientBrand", back_populates="components")
    inventory_items = relationship("NutrientInventory", back_populates="component")

    def __repr__(self):
        return f"<NutrientComponent {self.name} ({self.brand.name if self.brand else 'N/A'})>"


class NutrientFormula(Base):
    """Feeding formulas for specific brand/stage/medium combinations."""
    __tablename__ = "nutrient_formulas"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("nutrient_brands.id"), nullable=False)
    growth_stage = Column(String(50), nullable=False)  # 'seedling', 'early_veg', 'late_veg', 'early_flower', 'mid_flower', 'late_flower', 'flush'
    medium = Column(String(50), nullable=False)  # 'hydro', 'coco', 'soil', 'inert'
    
    # Ratios stored as JSON: {component_id: ml_per_liter}
    ratios = Column(JSON, nullable=False)
    
    # Target ranges
    ppm_target_min = Column(Float)
    ppm_target_max = Column(Float)
    ec_target_min = Column(Float)  # EC in mS/cm
    ec_target_max = Column(Float)
    ph_target_min = Column(Float)
    ph_target_max = Column(Float)
    
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    brand = relationship("NutrientBrand", back_populates="formulas")

    def __repr__(self):
        return f"<NutrientFormula {self.brand.name if self.brand else 'N/A'} - {self.growth_stage} ({self.medium})>"


class WaterSource(Base):
    """User's water source configuration."""
    __tablename__ = "water_sources"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_type = Column(String(50), nullable=False)  # 'tap', 'distilled', 'ro', 're_mineralized'
    ppm_base = Column(Float, default=0.0)  # Starting PPM before nutrients
    ph_base = Column(Float)  # Starting pH
    hardness = Column(String(20))  # 'soft', 'medium', 'hard'
    requires_calmag = Column(Boolean, default=False)
    notes = Column(Text)
    active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<WaterSource {self.source_type} (User {self.user_id})>"


class NutrientInventory(Base):
    """User's nutrient inventory/stash."""
    __tablename__ = "nutrient_inventory"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    component_id = Column(Integer, ForeignKey("nutrient_components.id"), nullable=False)
    
    quantity_ml = Column(Float, nullable=False, default=0.0)  # Current remaining
    original_quantity_ml = Column(Float)  # Bottle size
    
    purchase_date = Column(Date)
    expiry_date = Column(Date)
    cost = Column(Float)
    
    low_stock_threshold = Column(Float, default=100.0)  # Alert when below this
    notes = Column(Text)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    component = relationship("NutrientComponent", back_populates="inventory_items")
    transactions = relationship("InventoryTransaction", back_populates="inventory_item", cascade="all, delete-orphan")

    @property
    def is_low_stock(self) -> bool:
        """Check if inventory is low."""
        return self.quantity_ml <= self.low_stock_threshold

    @property
    def percentage_remaining(self) -> Optional[float]:
        """Calculate percentage remaining."""
        if self.original_quantity_ml and self.original_quantity_ml > 0:
            return (self.quantity_ml / self.original_quantity_ml) * 100
        return None

    def __repr__(self):
        return f"<NutrientInventory {self.component.name if self.component else 'N/A'} - {self.quantity_ml}ml>"


class InventoryTransaction(Base):
    """Track nutrient inventory usage and restocking."""
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey("nutrient_inventory.id"), nullable=False)
    transaction_type = Column(String(20), nullable=False)  # 'use', 'restock', 'adjust'
    quantity_ml = Column(Float, nullable=False)  # Positive for restock, negative for use
    feeding_log_id = Column(Integer, ForeignKey("feeding_logs.id"), nullable=True)  # If from feeding
    
    transaction_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = Column(Text)

    # Relationships
    inventory_item = relationship("NutrientInventory", back_populates="transactions")

    def __repr__(self):
        return f"<InventoryTransaction {self.transaction_type} - {self.quantity_ml}ml>"


class FeedingSchedule(Base):
    """Feeding schedule for a plant."""
    __tablename__ = "feeding_schedules"

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("nutrient_brands.id"), nullable=False)
    
    start_date =  Column(Date)
    schedule_type = Column(String(20), default='weekly')  # 'weekly', 'biweekly', 'custom'
    active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    brand = relationship("NutrientBrand")

    def __repr__(self):
        return f"<FeedingSchedule Plant {self.plant_id} - {self.brand.name if self.brand else 'N/A'}>"


class FeedingLog(Base):
    """Historical record of plant feedings."""
    __tablename__ = "feeding_logs"

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("nutrient_brands.id"), nullable=False)
    
    fed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    volume_liters = Column(Float)
    ppm_actual = Column(Float)
    ph_actual = Column(Float)
    
    # What was actually mixed: {component_id: ml_amount}
    ratios_used = Column(JSON)
    
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    brand = relationship("NutrientBrand")
    transactions = relationship("InventoryTransaction", backref="feeding_log")

    def __repr__(self):
        return f"<FeedingLog Plant {self.plant_id} - {self.fed_at}>"
