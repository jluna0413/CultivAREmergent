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


# Note: check_password function removed as it was unused and incompatible
# with the current password hashing scheme used in the application.
# Password verification is handled by the User model's check_password method.
