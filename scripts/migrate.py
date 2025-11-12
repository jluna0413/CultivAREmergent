"""Run Alembic database migrations for CultivAR."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config


def _configure_alembic() -> Config:
    """Load the Alembic configuration relative to the project root."""
    project_root = Path(__file__).resolve().parents[1]
    alembic_ini = project_root / "alembic.ini"
    if not alembic_ini.exists():
        raise FileNotFoundError("Could not find alembic.ini at project root")

    config = Config(str(alembic_ini))
    script_location = project_root / "alembic"
    config.set_main_option("script_location", str(script_location))
    return config


def main() -> None:
    """Upgrade the database schema to the latest revision."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    logger = logging.getLogger("scripts.migrate")

    try:
        config = _configure_alembic()
        logger.info("Applying Alembic migrations (upgrade head)")
        command.upgrade(config, "head")
    except Exception as exc:  # pragma: no cover - failure path
        logger.exception("Alembic migration failed")
        sys.exit(1)
    else:
        logger.info("Database schema is up to date")


if __name__ == "__main__":
    main()
