"""
Authentication utilities for the CultivAR application.
"""
import bcrypt

from app.logger import logger

# def hash_password(password): #commented out
#    """
#    Hash a password using bcrypt.
#
#    Args:
#        password (str): The password to hash.
#
#    Returns:
#        str: The hashed password.
#    """
#    try:
#        # Generate a salt and hash the password
#        password_bytes = password.encode('utf-8')
#        salt = bcrypt.gensalt()
#        hashed = bcrypt.hashpw(password_bytes, salt)
#        return hashed.decode('utf-8')
#    except Exception as e:
#        logger.error(f"Error hashing password: {e}")
#        return None


def check_password(password, hashed_password):
    """
    Check if a password matches a hash.

    Args:
        password (str): The password to check.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    try:
        # Check if the password matches the hash
        password_bytes = password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logger.error(f"Error checking password: {e}")
        return False
