"""
Base database models for the CultivAR application.
"""

from datetime import datetime

from flask_login import UserMixin
import bcrypt
from werkzeug.security import (
    check_password_hash,  # Import hashing functions
    generate_password_hash,
)

from app.models import db


class User(db.Model, UserMixin):
    """User model for authentication."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(
        db.String(128), nullable=False
    )  # Renamed to password_hash
    phone = db.Column(db.String(20))  # Phone number field
    email = db.Column(db.String(120))  # Email field
    force_password_change = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add is_admin field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, username=None, phone=None, email=None, password_hash=None, is_admin=False, force_password_change=False, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.phone = phone
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.force_password_change = force_password_change

    def set_password(self, password):
        """Hashes the password and sets the password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)


class PlantActivity(db.Model):
    """Plant activity model."""

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False)

    # Relationships
    activity = db.relationship("Activity", backref="plant_activities")


class Activity(db.Model):
    """Activity type model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Breeder(db.Model):
    """Breeder model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class Measurement(db.Model):
    """Plant measurement model."""

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey("metric.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    metric = db.relationship("Metric", backref="measurements")


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
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    cultivar_id = db.Column(db.Integer, db.ForeignKey("cultivar.id"))
    zone_id = db.Column(db.Integer, db.ForeignKey("zone.id"))
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
    cultivar_url = db.Column(db.String(255))
    est_harvest_date = db.Column(db.DateTime)
    autoflower = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("plant.id"))

    # Relationships
    status = db.relationship("Status", foreign_keys=[status_id], backref="plants")
    cultivar = db.relationship("Cultivar", backref="plants")
    zone = db.relationship("Zone", backref="plants")
    measurements = db.relationship(
        "Measurement", backref="plant", cascade="all, delete-orphan"
    )
    activities = db.relationship(
        "PlantActivity", backref="plant", cascade="all, delete-orphan"
    )
    images = db.relationship(
        "PlantImage", backref="plant", cascade="all, delete-orphan"
    )
    parent = db.relationship("Plant", remote_side=[id], backref="children")

    @property
    def status_name(self):
        return self.status.status if self.status else None

    @property
    def cultivar_name(self):
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

    def __init__(self, name=None, description=None, status_id=None, cultivar_id=None, zone_id=None, current_day=0, current_week=0, current_height=None, height_date=None, last_water_date=None, last_feed_date=None, is_clone=False, start_dt=None, harvest_weight=None, harvest_date=None, cycle_time=None, cultivar_url=None, est_harvest_date=None, autoflower=False, parent_id=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.status_id = status_id
        self.cultivar_id = cultivar_id
        self.zone_id = zone_id
        self.current_day = current_day
        self.current_week = current_week
        self.current_height = current_height
        self.height_date = height_date
        self.last_water_date = last_water_date
        self.last_feed_date = last_feed_date
        self.is_clone = is_clone
        self.start_dt = start_dt or datetime.utcnow()
        self.harvest_weight = harvest_weight
        self.harvest_date = harvest_date
        self.cycle_time = cycle_time
        self.cultivar_url = cultivar_url
        self.est_harvest_date = est_harvest_date
        self.autoflower = autoflower
        self.parent_id = parent_id

    @property
    def latest_image(self):
        return (
            PlantImage.query.filter_by(plant_id=self.id)
            .order_by(PlantImage.image_date.desc())
            .first()
        )


class PlantImage(db.Model):
    """Plant image model."""

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    image_description = db.Column(db.Text)
    image_order = db.Column(db.Integer, default=0)
    image_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Sensor(db.Model):
    """Sensor model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey("zone.id"))
    source = db.Column(db.String(50))
    device = db.Column(db.String(100))
    type = db.Column(db.String(50))
    show = db.Column(db.Boolean, default=True)
    unit = db.Column(db.String(20))
    ac_infinity_device_id = db.Column(
        db.Integer, db.ForeignKey("ac_infinity_device.id")
    )
    ecowitt_device_id = db.Column(db.Integer, db.ForeignKey("ecowitt_device.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships - remove conflicting backref
    zone = db.relationship("Zone", backref="sensors")
    data = db.relationship("SensorData", back_populates="sensor", cascade="all, delete-orphan")

    @property
    def zone_name(self):
        return self.zone.name if self.zone else None


class SensorData(db.Model):
    """Sensor data model."""

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id"), nullable=False)
    value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships - remove conflicting backref
    sensor = db.relationship("Sensor", back_populates="data")

    @property
    def sensor_name(self):
        return self.sensor.name if self.sensor else None


class Settings(db.Model):
    """Settings model."""

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Status(db.Model):
    """Plant status model."""

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

    # For status history
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship for status history
    plant = db.relationship(
        "Plant",
        foreign_keys=[plant_id],
        backref="status_history",
        overlaps="plants,status",
    )


class Cultivar(db.Model):
    """Cannabis cultivar model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breeder_id = db.Column(db.Integer, db.ForeignKey("breeder.id"))
    indica = db.Column(db.Integer, default=0)
    sativa = db.Column(db.Integer, default=0)
    autoflower = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    seed_count = db.Column(db.Integer, default=0)
    cycle_time = db.Column(db.Integer)
    url = db.Column(db.String(255))
    short_description = db.Column(db.Text)

    # Relationships
    breeder = db.relationship("Breeder", backref="cultivars")

    def __init__(self, name=None, breeder_id=None, indica=0, sativa=0, autoflower=False, description=None, seed_count=0, cycle_time=None, url=None, short_description=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.breeder_id = breeder_id
        self.indica = indica
        self.sativa = sativa
        self.autoflower = autoflower
        self.description = description
        self.seed_count = seed_count
        self.cycle_time = cycle_time
        self.url = url
        self.short_description = short_description

    @property
    def breeder_name(self):
        return self.breeder.name if self.breeder else None


class Zone(db.Model):
    """Growing zone model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class Stream(db.Model):
    """Video stream model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey("zone.id"))
    visible = db.Column(db.Boolean, default=True)

    # Relationships
    zone = db.relationship("Zone", backref="streams")

    @property
    def zone_name(self):
        return self.zone.name if self.zone else None


# Marketing-related models for the marketing website

class Waitlist(db.Model):
    """Waitlist model for pre-launch signups."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    priority_tier = db.Column(db.String(20), default='general')  # early_bird, beta, general
    referral_code = db.Column(db.String(20), unique=True)
    referred_by = db.Column(db.Integer, db.ForeignKey('waitlist.id'))
    signup_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_activated = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45))  # For tracking unique signups
    user_agent = db.Column(db.String(255))  # For analytics

    # Relationships
    referred_users = db.relationship('Waitlist', backref='referrer', remote_side=[id])

    def __init__(self, email=None, priority_tier='general', **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.priority_tier = priority_tier

    @property
    def referral_count(self):
        from app.models import db
        return db.session.query(Waitlist).filter_by(referred_by=self.id).count()

    @property
    def signup_date_formatted(self):
        return self.signup_date.strftime('%B %d, %Y') if self.signup_date else None


class BlogPost(db.Model):
    """Blog post model for content marketing."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    category = db.Column(db.String(50))  # growing_tips, cultivar_reviews, industry_news, etc.
    author = db.Column(db.String(100))
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    featured_image = db.Column(db.String(255))  # Path to featured image
    meta_description = db.Column(db.String(160))  # SEO meta description
    tags = db.Column(db.String(255))  # Comma-separated tags
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title=None, slug=None, content=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.slug = slug
        self.content = content

    @property
    def publish_date_formatted(self):
        return self.publish_date.strftime('%B %d, %Y') if self.publish_date else None

    @property
    def reading_time(self):
        """Estimate reading time in minutes."""
        if not self.content:
            return 0
        words_per_minute = 200
        word_count = len(self.content.split())
        return max(1, round(word_count / words_per_minute))

    @property
    def tags_list(self):
        """Return tags as a list."""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []


class LeadMagnet(db.Model):
    """Lead magnet model for tracking downloads."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Beginners Grow Book"
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255), nullable=False)  # Path to downloadable file
    download_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name=None, file_path=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.file_path = file_path


class LeadMagnetDownload(db.Model):
    """Track individual lead magnet downloads."""

    id = db.Column(db.Integer, primary_key=True)
    lead_magnet_id = db.Column(db.Integer, db.ForeignKey('lead_magnet.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(45))
    download_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.String(255))

    # Relationships
    lead_magnet = db.relationship('LeadMagnet', backref='downloads')

    def __init__(self, lead_magnet_id=None, email=None, **kwargs):
        super().__init__(**kwargs)
        self.lead_magnet_id = lead_magnet_id
        self.email = email


class NewsletterSubscriber(db.Model):
    """Enhanced newsletter subscriber model supporting both email and phone."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    subscription_type = db.Column(db.String(20), default='both')  # email, phone, both
    is_active = db.Column(db.Boolean, default=True)
    subscription_date = db.Column(db.DateTime, default=datetime.utcnow)
    unsubscribe_date = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))
    preferences = db.Column(db.Text)  # JSON string of user preferences
    source = db.Column(db.String(50))  # landing_page, blog_post, etc.

    def __init__(self, email=None, phone=None, subscription_type='both', **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.phone = phone
        self.subscription_type = subscription_type

    @property
    def contact_info(self):
        """Return the primary contact method."""
        if self.email:
            return self.email
        elif self.phone:
            return self.phone
        return None

    @property
    def is_unsubscribed(self):
        return self.unsubscribe_date is not None


# Backward compatibility alias
Strain = Cultivar
