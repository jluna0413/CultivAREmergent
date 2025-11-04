"""
Script to populate the CultivAR database with sample data.
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the current directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Flask app and models
from main import create_app
from app.models import db
from app.models.base_models import (
    Breeder, Cultivar, Zone, Status, Activity, Metric,
    Plant, Sensor, SensorData, Settings
)

def populate_breeders():
    """Add sample breeders to the database."""
    breeders = [
        {"name": "Barney's Farm"},
        {"name": "Dutch Passion"},
        {"name": "Humboldt Seeds"},
        {"name": "Mephisto Genetics"},
        {"name": "Sweet Seeds"},
        {"name": "FastBuds"},
        {"name": "Royal Queen Seeds"},
        {"name": "Seedsman"}
    ]

    for breeder_data in breeders:
        # Check if breeder already exists
        if not Breeder.query.filter_by(name=breeder_data["name"]).first():
            breeder = Breeder(**breeder_data)
            db.session.add(breeder)

    db.session.commit()
    print(f"Added {len(breeders)} breeders")

def populate_cultivars():
    """Add sample cultivars to the database."""
    cultivars = [
        {
            "name": "Wedding Cake",
            "breeder_name": "Barney's Farm",
            "indica": 70,
            "sativa": 30,
            "autoflower": False,
            "description": "Wedding Cake is a potent indica-hybrid cultivar known for its rich and tangy flavor profile with earthy and peppery notes. The buds are dense, colorful and coated with trichomes. Effects are relaxing and euphoric, making it ideal for evening use.",
            "short_description": "Cherry Pie x Girl Scout Cookies",
            "seed_count": 5,
            "cycle_time": 63,
            "url": "https://www.barneysfarm.com/wedding-cake-466",
            "price": 52.00
        },
        {
            "name": "Blueberry",
            "breeder_name": "Dutch Passion",
            "indica": 80,
            "sativa": 20,
            "autoflower": False,
            "description": "Blueberry is a classic indica cultivar that has been popular since the 1970s. It's known for its sweet berry aroma and flavor. The effects are deeply relaxing and long-lasting, perfect for stress relief and insomnia.",
            "short_description": "Thai x Purple Thai x Afghani",
            "seed_count": 3,
            "cycle_time": 56,
            "url": "https://dutch-passion.com/en/cannabis-seeds/blueberry",
            "price": 45.00
        },
        {
            "name": "Gorilla Glue Auto",
            "breeder_name": "FastBuds",
            "indica": 50,
            "sativa": 50,
            "autoflower": True,
            "description": "Gorilla Glue Auto is a balanced hybrid with high THC content. It produces dense, resin-covered buds with a strong earthy and pine aroma. The effects are powerful and long-lasting, combining cerebral stimulation with physical relaxation.",
            "short_description": "Gorilla Glue #4 x Ruderalis",
            "seed_count": 7,
            "cycle_time": 70,
            "url": "https://2fast4buds.com/seeds/gorilla-glue-auto",
            "price": 42.50
        },
        {
            "name": "Northern Lights",
            "breeder_name": "Royal Queen Seeds",
            "indica": 90,
            "sativa": 10,
            "autoflower": False,
            "description": "Northern Lights is one of the most famous indica cultivars of all time. It produces resinous buds with a sweet and spicy aroma. The effects are deeply relaxing and sedating, perfect for evening use and sleep aid.",
            "short_description": "Afghani x Thai",
            "seed_count": 10,
            "cycle_time": 49,
            "url": "https://www.royalqueenseeds.com/indica-cannabis-seeds/53-northern-light.html",
            "price": 40.00
        },
        {
            "name": "Sour Diesel",
            "breeder_name": "Humboldt Seeds",
            "indica": 40,
            "sativa": 60,
            "autoflower": False,
            "description": "Sour Diesel is a sativa-dominant cultivar known for its pungent diesel aroma. It provides energetic and uplifting effects that are great for daytime use, creativity, and social activities.",
            "short_description": "Chemdawg x Super Skunk",
            "seed_count": 6,
            "cycle_time": 70,
            "url": "https://humboldtseeds.net/en/sour-diesel/",
            "price": 48.00
        },
        {
            "name": "Double Grape",
            "breeder_name": "Mephisto Genetics",
            "indica": 70,
            "sativa": 30,
            "autoflower": True,
            "description": "Double Grape is an indica-dominant autoflower with a sweet grape aroma and flavor. It produces dense, purple-tinged buds with high resin production. The effects are relaxing and euphoric.",
            "short_description": "Sour Stomper x Grape Crinkle",
            "seed_count": 3,
            "cycle_time": 65,
            "url": "https://www.mephistogenetics.com/seeds/double-grape",
            "price": 55.00
        }
    ]

    for cultivar_data in cultivars:
        # Get breeder ID
        breeder_name = cultivar_data.pop("breeder_name")
        breeder = Breeder.query.filter_by(name=breeder_name).first()

        if breeder:
            # Check if cultivar already exists
            if not Cultivar.query.filter_by(name=cultivar_data["name"]).first():
                # Remove price as it's not in the model
                price = cultivar_data.pop("price", None)

                cultivar = Cultivar(breeder_id=breeder.id, **cultivar_data)
                db.session.add(cultivar)

    db.session.commit()
    print(f"Added {len(cultivars)} cultivars")

def populate_zones():
    """Add sample growing zones to the database."""
    zones = [
        {"name": "Veg Tent"},
        {"name": "Flower Tent"},
        {"name": "Seedling Area"},
        {"name": "Drying Room"},
        {"name": "Clone Station"}
    ]

    for zone_data in zones:
        # Check if zone already exists
        if not Zone.query.filter_by(name=zone_data["name"]).first():
            zone = Zone(**zone_data)
            db.session.add(zone)

    db.session.commit()
    print(f"Added {len(zones)} zones")

def populate_statuses():
    """Add plant status options to the database."""
    statuses = [
        {"status": "Seedling"},
        {"status": "Vegetative"},
        {"status": "Flowering"},
        {"status": "Harvested"},
        {"status": "Curing"},
        {"status": "Completed"},
        {"status": "Dead"}
    ]

    for status_data in statuses:
        # Check if status already exists
        if not Status.query.filter_by(status=status_data["status"]).first():
            status = Status(**status_data)
            db.session.add(status)

    db.session.commit()
    print(f"Added {len(statuses)} statuses")

def populate_activities():
    """Add plant activity types to the database."""
    activities = [
        {"name": "Watering"},
        {"name": "Feeding"},
        {"name": "Training"},
        {"name": "Pruning"},
        {"name": "Transplanting"},
        {"name": "Pest Treatment"},
        {"name": "Defoliation"},
        {"name": "Flushing"},
        {"name": "Harvesting"},
        {"name": "Note"}
    ]

    for activity_data in activities:
        # Check if activity already exists
        if not Activity.query.filter_by(name=activity_data["name"]).first():
            activity = Activity(**activity_data)
            db.session.add(activity)

    db.session.commit()
    print(f"Added {len(activities)} activities")

def populate_metrics():
    """Add measurement metrics to the database."""
    metrics = [
        {"name": "Height", "unit": "cm"},
        {"name": "Width", "unit": "cm"},
        {"name": "pH", "unit": "pH"},
        {"name": "EC", "unit": "mS/cm"},
        {"name": "PPM", "unit": "ppm"},
        {"name": "Temperature", "unit": "°C"},
        {"name": "Humidity", "unit": "RH%"},
        {"name": "CO2", "unit": "ppm"},
        {"name": "Light Intensity", "unit": "lux"}
    ]

    for metric_data in metrics:
        # Check if metric already exists
        if not Metric.query.filter_by(name=metric_data["name"]).first():
            metric = Metric(**metric_data)
            db.session.add(metric)

    db.session.commit()
    print(f"Added {len(metrics)} metrics")

def populate_sensors():
    """Add sample sensors to the database."""
    # Get zones
    veg_tent = Zone.query.filter_by(name="Veg Tent").first()
    flower_tent = Zone.query.filter_by(name="Flower Tent").first()

    if not veg_tent or not flower_tent:
        print("Zones not found. Please run populate_zones() first.")
        return

    sensors = [
        {
            "name": "Veg Temp",
            "zone_id": veg_tent.id,
            "source": "Manual",
            "device": "Thermometer",
            "type": "Temperature",
            "unit": "°C"
        },
        {
            "name": "Veg Humidity",
            "zone_id": veg_tent.id,
            "source": "Manual",
            "device": "Hygrometer",
            "type": "Humidity",
            "unit": "RH%"
        },
        {
            "name": "Flower Temp",
            "zone_id": flower_tent.id,
            "source": "Manual",
            "device": "Thermometer",
            "type": "Temperature",
            "unit": "°C"
        },
        {
            "name": "Flower Humidity",
            "zone_id": flower_tent.id,
            "source": "Manual",
            "device": "Hygrometer",
            "type": "Humidity",
            "unit": "RH%"
        }
    ]

    for sensor_data in sensors:
        # Check if sensor already exists
        existing_sensor = Sensor.query.filter_by(name=sensor_data["name"]).first()
        if not existing_sensor:
            sensor = Sensor(**sensor_data)
            db.session.add(sensor)
            db.session.commit()  # Commit to get the sensor ID

            # Add some sample data points
            now = datetime.now()  # Use datetime.now() instead of utcnow()
            for i in range(24):  # 24 hours of data
                time_point = now - timedelta(hours=i)

                if "Temp" in sensor_data["name"]:
                    # Temperature between 20-28°C
                    value = round(random.uniform(20, 28), 1)
                else:
                    # Humidity between 40-65%
                    value = round(random.uniform(40, 65), 1)

                data_point = SensorData(
                    sensor_id=sensor.id,
                    value=value,
                    created_at=time_point
                )
                db.session.add(data_point)

            db.session.commit()  # Commit after adding all data points for this sensor

    print(f"Added {len(sensors)} sensors with sample data")

def populate_plants():
    """Add sample plants to the database."""
    # Get cultivars
    wedding_cake = Cultivar.query.filter_by(name="Wedding Cake").first()
    blueberry = Cultivar.query.filter_by(name="Blueberry").first()

    # Get zones
    veg_tent = Zone.query.filter_by(name="Veg Tent").first()
    flower_tent = Zone.query.filter_by(name="Flower Tent").first()

    # Get statuses
    seedling_status = Status.query.filter_by(status="Seedling").first()
    veg_status = Status.query.filter_by(status="Vegetative").first()
    flower_status = Status.query.filter_by(status="Flowering").first()

    if not wedding_cake or not blueberry or not veg_tent or not flower_tent or not seedling_status or not veg_status or not flower_status:
        print("Required data not found. Please run other populate functions first.")
        return

    now = datetime.now()

    plants = [
        {
            "name": "WC #1",
            "description": "Wedding Cake plant, started from seed.",
            "status_id": seedling_status.id,
            "cultivar_id": wedding_cake.id,
            "zone_id": veg_tent.id,
            "current_day": 7,
            "current_week": 1,
            "current_height": "5 cm",
            "is_clone": False,
            "start_dt": now - timedelta(days=7)
        },
        {
            "name": "BB #1",
            "description": "Blueberry plant, started from seed.",
            "status_id": veg_status.id,
            "cultivar_id": blueberry.id,
            "zone_id": veg_tent.id,
            "current_day": 21,
            "current_week": 3,
            "current_height": "25 cm",
            "is_clone": False,
            "start_dt": now - timedelta(days=21)
        },
        {
            "name": "WC #2",
            "description": "Wedding Cake plant, in flowering stage.",
            "status_id": flower_status.id,
            "cultivar_id": wedding_cake.id,
            "zone_id": flower_tent.id,
            "current_day": 42,
            "current_week": 6,
            "current_height": "60 cm",
            "is_clone": False,
            "start_dt": now - timedelta(days=42)
        }
    ]

    for plant_data in plants:
        # Check if plant already exists
        if not Plant.query.filter_by(name=plant_data["name"]).first():
            plant = Plant(**plant_data)
            db.session.add(plant)

    db.session.commit()
    print(f"Added {len(plants)} plants")

def populate_settings():
    """Add default settings to the database."""
    settings = [
        {"key": "app_name", "value": "CultivAR"},
        {"key": "theme", "value": "dark"},
        {"key": "temperature_unit", "value": "celsius"},
        {"key": "default_view", "value": "dashboard"},
        {"key": "notifications_enabled", "value": "true"},
        {"key": "email_notifications", "value": "false"},
        {"key": "data_retention_days", "value": "90"}
    ]

    for setting_data in settings:
        # Check if setting already exists
        if not Settings.query.filter_by(key=setting_data["key"]).first():
            setting = Settings(**setting_data)
            db.session.add(setting)

    db.session.commit()
    print(f"Added {len(settings)} settings")

def main():
    """Main function to populate the database."""
    app = create_app()

    with app.app_context():
        print("Starting database population...")

        # Populate the database with sample data
        populate_breeders()
        populate_cultivars()
        populate_zones()
        populate_statuses()
        populate_activities()
        populate_metrics()
        populate_sensors()
        populate_plants()
        populate_settings()

        print("Database population completed!")

if __name__ == "__main__":
    main()
