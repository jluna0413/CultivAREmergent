"""
Input validation and sanitization utilities for the CultivAR application.
"""

import re
from typing import Optional, Tuple

import bleach

# Configuration for bleach sanitization
ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "blockquote",
    "code",
    "pre",
    "a",
    "img",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
}


def sanitize_html(text: str) -> str:
    """
    Sanitize HTML content to prevent XSS attacks.

    Args:
        text (str): The text to sanitize.

    Returns:
        str: Sanitized text with only allowed HTML tags.
    """
    if not text:
        return ""

    return bleach.clean(
        text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
    )


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format and requirements.

    Args:
        email (str): The email address to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not email:
        return False, "Email address is required"

    if not isinstance(email, str):
        return False, "Email must be a string"

    email = email.strip()

    if len(email) > 254:  # RFC 3696 limit
        return False, "Email address is too long"

    # Basic email regex (RFC 5322 compliant-ish)
    email_pattern = r"^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    return True, ""


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username requirements.

    Args:
        username (str): The username to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"

    if not isinstance(username, str):
        return False, "Username must be a string"

    username = username.strip()

    if len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if len(username) > 30:
        return False, "Username must be less than 30 characters long"

    # Allow alphanumeric, hyphens, underscores, and spaces
    username_pattern = r"^[a-zA-Z0-9_-]+$"

    if not re.match(username_pattern, username):
        return (
            False,
            "Username can only contain letters, numbers, hyphens, and underscores",
        )

    # Check for common reserved usernames
    reserved_usernames = {
        "admin",
        "root",
        "system",
        "user",
        "test",
        "api",
        "www",
        "mail",
        "ftp",
    }
    if username.lower() in reserved_usernames:
        return False, "This username is not allowed"

    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength requirements.

    Args:
        password (str): The password to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"

    if not isinstance(password, str):
        return False, "Password must be a string"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 128:
        return False, "Password must be less than 128 characters long"

    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    # Check for at least one digit
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return (
            False,
            'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)',
        )

    return True, ""


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number format.

    Args:
        phone (str): The phone number to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not phone:
        return True, ""  # Phone is optional

    if not isinstance(phone, str):
        return False, "Phone must be a string"

    phone = phone.strip()

    # Remove common formatting characters
    phone_clean = re.sub(r"[\s\-\(\)\.+]", "", phone)

    # Check if length is reasonable for a phone number
    if len(phone_clean) < 10 or len(phone_clean) > 15:
        return False, "Phone number must be between 10 and 15 digits"

    # Check if it's all digits
    if not re.match(r"^\d+$", phone_clean):
        return False, "Phone number can only contain digits"

    return True, ""


def sanitize_text_field(text: str, field_name: str = "text") -> Tuple[str, str]:
    """
    Sanitize text field input and return sanitized value.

    Args:
        text (str): The text to sanitize.
        field_name (str): Name of the field for error messages.

    Returns:
        Tuple[str, str]: (sanitized_text, error_message)
    """
    if not text:
        return "", ""

    if not isinstance(text, str):
        return "", f"{field_name} must be a string"

    if len(text) > 5000:  # Reasonable limit for text fields
        return "", f"{field_name} is too long (max 5000 characters)"

    sanitized = sanitize_html(text)

    # Check if content was overly maligned (e.g., lots of scripts removed)
    if len(sanitized) < (len(text) * 0.5) and len(text) > 100:
        # This might indicate script tags or other malicious content was removed
        return (
            sanitized,
            f"{field_name} contained potentially unsafe content that was removed",
        )

    return sanitized, ""


def cleanse_user_data(data: dict) -> Tuple[dict, list]:
    """
    Cleanse and validate user data dictionary.

    Args:
        data (dict): User data to cleanse.

    Returns:
        Tuple[dict, list]: (cleaned_data, error_messages)
    """
    errors = []

    # Copy data to avoid modifying original
    cleaned_data = data.copy()

    # Validate and sanitize username
    if "username" in data:
        is_valid, error = validate_username(data["username"])
        if not is_valid:
            errors.append(error)
        else:
            cleaned_data["username"] = data["username"].strip()

    # Validate and sanitize email
    if "email" in data:
        is_valid, error = validate_email(data["email"])
        if not is_valid:
            errors.append(error)
        else:
            cleaned_data["email"] = data["email"].strip().lower()

    # Validate password (but don't return it in cleaned data for security)
    if "password" in data:
        is_valid, error = validate_password(data["password"])
        if not is_valid:
            errors.append(error)

    # Validate and sanitize phone
    if "phone" in data:
        is_valid, error = validate_phone(data.get("phone", ""))
        if not is_valid:
            errors.append(error)
        else:
            cleaned_data["phone"] = data["phone"].strip() if data["phone"] else None

    return cleaned_data, errors
