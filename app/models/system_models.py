"""
System-wide models for the CultivAR application.
"""

from datetime import datetime
from app.models import db

class SystemActivity(db.Model):
    """System activity model for tracking system-wide activities."""
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # login, plant_add, strain_edit, etc.
    user = db.Column(db.String(80), nullable=False)  # Username
    details = db.Column(db.Text)  # JSON string with activity details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SystemActivity {self.type} by {self.user} at {self.timestamp}>"
