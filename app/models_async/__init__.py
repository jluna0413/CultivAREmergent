"""
Async SQLAlchemy Models Package
Pure async models without Flask dependencies.
"""

from app.models_async.base import Base, async_engine, AsyncSessionLocal, get_async_session
from app.models_async.auth import User
from app.models_async.grow import Plant, Cultivar, Breeder, Status, Grow, Metric, Zone
from app.models_async.activities import Activity, ActivitySummary, PlantActivity
from app.models_async.sensors import Sensor, SensorData, Stream
from app.models_async.marketing import (
    Waitlist,
    NewsletterSubscriber,
    BlogPost,
    LeadMagnet,
    LeadMagnetDownload,
)
from app.models_async.commerce import Order, Product, OrderItem
from app.models_async.settings import Settings, Extension
from app.models_async.measurements import Measurement
from app.models_async.plant_images import PlantImage
from app.models_async.system import SystemActivity

__all__ = [
    "Base",
    "async_engine",
    "AsyncSessionLocal",
    "get_async_session",
    "User",
    "Plant",
    "Cultivar",
    "Breeder",
    "Status",
    "Grow",
    "Metric",
    "Zone",
    "Activity",
    "ActivitySummary",
    "PlantActivity",
    "SystemActivity",
    "Sensor",
    "SensorData",
    "Stream",
    "Waitlist",
    "NewsletterSubscriber",
    "BlogPost",
    "LeadMagnet",
    "LeadMagnetDownload",
    "Measurement",
    "PlantImage",
    "Order",
    "Product",
    "OrderItem",
    "Settings",
    "Extension",
]
