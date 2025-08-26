"""
Helper utilities for the CultivAR application.
"""

import os
import re
from datetime import datetime, timedelta

from flask import jsonify, request

from app.logger import logger


def get_file_extension(filename):
    """
    Get the file extension from a filename.

    Args:
        filename (str): The filename to get the extension from.

    Returns:
        str: The file extension.
    """
    return os.path.splitext(filename)[1].lower()


def is_valid_image(filename):
    """
    Check if a file is a valid image based on its extension.

    Args:
        filename (str): The filename to check.

    Returns:
        bool: True if the file is a valid image, False otherwise.
    """
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    return get_file_extension(filename) in valid_extensions


def format_date(date):
    """
    Format a date as a string.

    Args:
        date (datetime): The date to format.

    Returns:
        str: The formatted date.
    """
    if not date:
        return ""
    return date.strftime("%m/%d/%Y")


def format_datetime(date):
    """
    Format a datetime as a string.

    Args:
        date (datetime): The datetime to format.

    Returns:
        str: The formatted datetime.
    """
    if not date:
        return ""
    return date.strftime("%m/%d/%Y %I:%M %p")


def parse_date(date_str):
    """
    Parse a date string into a datetime object.

    Args:
        date_str (str): The date string to parse.

    Returns:
        datetime: The parsed date.
    """
    try:
        # Try different date formats
        formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %I:%M %p",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # If we get here, none of the formats worked
        logger.warning(f"Could not parse date: {date_str}")
        return None
    except Exception as e:
        logger.error(f"Error parsing date: {e}")
        return None


def calculate_days_since(date):
    """
    Calculate the number of days since a date.

    Args:
        date (datetime): The date to calculate from.

    Returns:
        int: The number of days since the date.
    """
    if not date:
        return None

    now = datetime.now()
    delta = now - date
    return delta.days


def calculate_weeks_since(date):
    """
    Calculate the number of weeks since a date.

    Args:
        date (datetime): The date to calculate from.

    Returns:
        int: The number of weeks since the date.
    """
    days = calculate_days_since(date)
    if days is None:
        return None

    return days // 7


def slugify(text):
    """
    Convert a string to a URL-friendly slug.

    Args:
        text (str): The text to convert.

    Returns:
        str: The slugified text.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove non-alphanumeric characters
    text = re.sub(r"[^a-z0-9\s-]", "", text)

    # Replace spaces with hyphens
    text = re.sub(r"\s+", "-", text)

    # Remove multiple hyphens
    text = re.sub(r"-+", "-", text)

    # Remove leading/trailing hyphens
    text = text.strip("-")

    return text


def get_client_ip():
    """
    Get the client's IP address.

    Returns:
        str: The client's IP address.
    """
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr


def estimate_harvest_date(start_date, cycle_time, autoflower=False):
    """
    Estimate the harvest date based on the start date and cycle time.

    Args:
        start_date (datetime): The start date.
        cycle_time (int): The cycle time in days.
        autoflower (bool): Whether the plant is an autoflower.

    Returns:
        datetime: The estimated harvest date.
    """
    if not start_date or not cycle_time:
        return None

    # For autoflowers, the cycle time is from seed to harvest
    if autoflower:
        return start_date + timedelta(days=cycle_time)

    # For photoperiod plants, assume 4 weeks of veg before the cycle time (which is flowering time)
    veg_time = 28  # 4 weeks in days
    return start_date + timedelta(days=veg_time + cycle_time)
