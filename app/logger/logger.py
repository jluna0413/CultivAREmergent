"""
Logger configuration for the CultivAR application.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Create logger
logger = logging.getLogger("cultivar")
logger.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Create file handler if logs directory exists
logs_dir = "logs"
if not os.path.exists(logs_dir):
    try:
        os.makedirs(logs_dir)
    except Exception as e:
        logger.warning(f"Could not create logs directory: {e}")

log_file = os.path.join(logs_dir, "cultivar.log")
try:
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning(f"Could not create log file: {e}")


def init_logger():
    """Initialize the logger."""
    logger.info("Logger initialized")


# Initialize logger
init_logger()
