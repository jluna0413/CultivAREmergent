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
    """Generate a new migration revision based on model changes."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    logger = logging.getLogger("scripts.generate_migration")

    try:
        config = _configure_alembic()
        message = input("Enter migration message: ") if len(sys.argv) < 2 else sys.argv[1]
        logger.info(f"Generating new migration: {message}")
        command.revision(config, message=message, autogenerate=True)
    except Exception as exc:
        logger.exception("Alembic revision generation failed")
        sys.exit(1)
    else:
        logger.info("Migration revision generated successfully")

if __name__ == "__main__":
    main()
