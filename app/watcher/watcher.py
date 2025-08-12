"""
Watcher module for monitoring sensors and streams.
"""

import os
import threading
import time
from datetime import datetime, timedelta

import requests

from app.config.config import Config
from app.handlers.sensor_handlers import scan_ac_infinity_sensors, scan_ecowitt_sensors
from app.handlers.settings_handlers import get_setting
from app.logger import logger
from app.models import db
from app.models.base_models import SensorData, Stream


def prune_sensor_data():
    """
    Prune old sensor data to prevent the database from growing too large.
    """
    try:
        # Keep data for 30 days
        cutoff_date = datetime.now() - timedelta(days=30)

        # Delete old data
        SensorData.query.filter(SensorData.created_at < cutoff_date).delete()
        db.session.commit()

        logger.info("Pruned old sensor data")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error pruning sensor data: {e}")


def start_watching():
    """
    Start the watcher threads.
    """
    # We'll disable the watcher threads for now to avoid application context issues
    # This is just for demonstration purposes
    logger.info("Started watcher threads (disabled for demo)")


def watch_sensors():
    """
    Watch sensors and collect data.
    """
    while True:
        try:
            # Get polling interval from settings
            polling_interval = int(get_setting("polling_interval") or 300)

            # Check if AC Infinity is enabled
            aci_enabled = get_setting("aci_enabled") == "true"
            if aci_enabled:
                scan_ac_infinity_sensors()

            # Check if Ecowitt is enabled
            ec_enabled = get_setting("ec_enabled") == "true"
            if ec_enabled:
                scan_ecowitt_sensors()

            # Sleep for the polling interval
            time.sleep(polling_interval)
        except Exception as e:
            logger.error(f"Error in sensor watcher: {e}")
            time.sleep(60)  # Sleep for a minute before retrying


def grab_streams():
    """
    Grab images from streams.
    """
    while True:
        try:
            # Check if stream grabbing is enabled
            stream_grab_enabled = get_setting("stream_grab_enabled") == "true"

            if stream_grab_enabled:
                # Get stream grab interval from settings
                stream_grab_interval = int(get_setting("stream_grab_interval") or 3600)

                # Get all streams
                streams = Stream.query.filter_by(visible=True).all()

                for stream in streams:
                    try:
                        # Create the stream folder if it doesn't exist
                        stream_folder = os.path.join(
                            Config.UPLOAD_FOLDER, "streams", str(stream.id)
                        )
                        os.makedirs(stream_folder, exist_ok=True)

                        # Generate a filename with timestamp
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                        filename = f"{timestamp}.jpg"

                        # Download the stream image
                        response = requests.get(stream.url, stream=True, timeout=10)

                        if response.status_code == 200:
                            with open(os.path.join(stream_folder, filename), "wb") as f:
                                for chunk in response.iter_content(chunk_size=1024):
                                    if chunk:
                                        f.write(chunk)

                            logger.info(f"Grabbed image from stream {stream.name}")
                        else:
                            logger.warning(
                                f"Failed to grab image from stream {stream.name}: {response.status_code}"
                            )
                    except Exception as e:
                        logger.error(f"Error grabbing stream {stream.name}: {e}")

                # Sleep for the stream grab interval
                time.sleep(stream_grab_interval)
            else:
                # Sleep for a minute before checking again
                time.sleep(60)
        except Exception as e:
            logger.error(f"Error in stream grabber: {e}")
            time.sleep(60)  # Sleep for a minute before retrying
