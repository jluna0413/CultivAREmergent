"""
Load configuration data from the database into the Config class.
"""

from app.config.config import Config
from app.logger import logger
from app.models.base_models import Activity, Breeder, Metric, Status, Cultivar, Zone


def load_config_from_db():
    """
    Load configuration data from the database into the Config class.
    This function should be called after the database is initialized.
    """
    try:
        # Load activities
        activities = Activity.query.all()
        Config.Activities = [{"id": a.id, "name": a.name} for a in activities]

        # Load metrics
        metrics = Metric.query.all()
        Config.Metrics = [{"id": m.id, "name": m.name, "unit": m.unit} for m in metrics]

        # Load statuses
        statuses = Status.query.all()
        Config.Statuses = [{"id": s.id, "status": s.status} for s in statuses]

        # Load zones
        zones = Zone.query.all()
        Config.Zones = [{"id": z.id, "name": z.name} for z in zones]

        # Load cultivars
        cultivars = Cultivar.query.all()
        Config.Cultivars = [
            {
                "id": c.id,
                "name": c.name,
                "breeder_id": c.breeder_id,
                "breeder_name": c.breeder_name,
                "indica": c.indica,
                "sativa": c.sativa,
                "autoflower": c.autoflower,
                "description": c.description,
                "seed_count": c.seed_count,
                "cycle_time": c.cycle_time,
                "url": c.url,
                "short_description": c.short_description,
            }
            for c in cultivars
        ]

        # Load breeders
        breeders = Breeder.query.all()
        Config.Breeders = [{"id": b.id, "name": b.name} for b in breeders]

        logger.info("Configuration loaded from database")
    except Exception as e:
        logger.error(f"Error loading configuration from database: {e}")
