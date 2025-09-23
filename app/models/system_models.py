"""
System-wide models for the CultivAR application.
"""

from datetime import datetime

from app.models import db


class SystemActivity(db.Model):
    """System activity model for tracking system-wide activities."""

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(
        db.String(50), nullable=False
    )  # login, plant_add, strain_edit, etc.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    details = db.Column(db.Text)  # JSON string with activity details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="system_activities")

    def __init__(self, user_id=None, type=None, details=None, timestamp=None):
        self.user_id = user_id
        self.type = type
        self.details = details
        self.timestamp = timestamp or datetime.utcnow()

    def __repr__(self):
        return (
            f"<SystemActivity {self.type} by {self.user.username} at {self.timestamp}>"
        )
