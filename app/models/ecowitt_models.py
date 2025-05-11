"""
Ecowitt specific models for the CultivAR application.
"""

from app.models import db
from datetime import datetime

class EcowittDevice(db.Model):
    """Ecowitt device model."""
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    ip_address = db.Column(db.String(15))
    mac_address = db.Column(db.String(17))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sensors = db.relationship('Sensor', backref='ecowitt_device', lazy=True)
