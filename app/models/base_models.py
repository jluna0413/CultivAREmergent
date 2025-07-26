"""
Base database models for the CultivAR application.
"""

from datetime import datetime
from flask_login import UserMixin
from app.models import db

from werkzeug.security import generate_password_hash, check_password_hash # Import hashing functions

class User(db.Model, UserMixin):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Renamed to password_hash
    force_password_change = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add is_admin field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        """Hashes the password and sets the password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

class PlantActivity(db.Model):
    """Plant activity model."""
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)

    # Relationships
    activity = db.relationship('Activity', backref='plant_activities')

class Activity(db.Model):
    """Activity type model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Breeder(db.Model):
    """Breeder model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Measurement(db.Model):
    """Plant measurement model."""
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    metric = db.relationship('Metric', backref='measurements')

class Metric(db.Model):
    """Measurement metric model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=False)

class Plant(db.Model):
    """Plant model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    strain_id = db.Column(db.Integer, db.ForeignKey('strain.id'))
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    current_day = db.Column(db.Integer, default=0)
    current_week = db.Column(db.Integer, default=0)
    current_height = db.Column(db.String(20))
    height_date = db.Column(db.DateTime)
    last_water_date = db.Column(db.DateTime)
    last_feed_date = db.Column(db.DateTime)
    is_clone = db.Column(db.Boolean, default=False)
    start_dt = db.Column(db.DateTime, default=datetime.utcnow)
    harvest_weight = db.Column(db.Float)
    harvest_date = db.Column(db.DateTime)
    cycle_time = db.Column(db.Integer)
    strain_url = db.Column(db.String(255))
    est_harvest_date = db.Column(db.DateTime)
    autoflower = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('plant.id'))

    # Relationships
    status = db.relationship('Status', foreign_keys=[status_id], backref='plants')
    strain = db.relationship('Strain', backref='plants')
    zone = db.relationship('Zone', backref='plants')
    measurements = db.relationship('Measurement', backref='plant', cascade='all, delete-orphan')
    activities = db.relationship('PlantActivity', backref='plant', cascade='all, delete-orphan')
    images = db.relationship('PlantImage', backref='plant', cascade='all, delete-orphan')
    parent = db.relationship('Plant', remote_side=[id], backref='children')

    @property
    def status_name(self):
        return self.status.status if self.status else None

    @property
    def strain_name(self):
        return self.strain.name if self.strain else None

    @property
    def breeder_name(self):
        return self.strain.breeder.name if self.strain and self.strain.breeder else None

    @property
    def zone_name(self):
        return self.zone.name if self.zone else None

    @property
    def parent_name(self):
        return self.parent.name if self.parent else None

    @property
    def latest_image(self):
        return PlantImage.query.filter_by(plant_id=self.id).order_by(PlantImage.image_date.desc()).first()

class PlantImage(db.Model):
    """Plant image model."""
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    image_description = db.Column(db.Text)
    image_order = db.Column(db.Integer, default=0)
    image_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Sensor(db.Model):
    """Sensor model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    source = db.Column(db.String(50))
    device = db.Column(db.String(100))
    type = db.Column(db.String(50))
    show = db.Column(db.Boolean, default=True)
    unit = db.Column(db.String(20))
    ac_infinity_device_id = db.Column(db.Integer, db.ForeignKey('ac_infinity_device.id'))
    ecowitt_device_id = db.Column(db.Integer, db.ForeignKey('ecowitt_device.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    zone = db.relationship('Zone', backref='sensors')
    data = db.relationship('SensorData', backref='sensor', cascade='all, delete-orphan')

    @property
    def zone_name(self):
        return self.zone.name if self.zone else None

class SensorData(db.Model):
    """Sensor data model."""
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def sensor_name(self):
        return self.sensor.name if self.sensor else None

class Settings(db.Model):
    """Settings model."""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Status(db.Model):
    """Plant status model."""
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

    # For status history
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship for status history
    plant = db.relationship('Plant', foreign_keys=[plant_id], backref='status_history', overlaps='plants,status')

class Strain(db.Model):
    """Cannabis strain model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breeder_id = db.Column(db.Integer, db.ForeignKey('breeder.id'))
    indica = db.Column(db.Integer, default=0)
    sativa = db.Column(db.Integer, default=0)
    autoflower = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    seed_count = db.Column(db.Integer, default=0)
    cycle_time = db.Column(db.Integer)
    url = db.Column(db.String(255))
    short_description = db.Column(db.Text)

    # Relationships
    breeder = db.relationship('Breeder', backref='strains')

    @property
    def breeder_name(self):
        return self.breeder.name if self.breeder else None

class Zone(db.Model):
    """Growing zone model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Stream(db.Model):
    """Video stream model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    visible = db.Column(db.Boolean, default=True)

    # Relationships
    zone = db.relationship('Zone', backref='streams')

    @property
    def zone_name(self):
        return self.zone.name if self.zone else None
