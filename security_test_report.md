# Security Test Report

**Generated:** 2025-09-09T19:49:30.544960

## Summary

- **Critical Issues:** 112
- **High Priority Issues:** 525
- **Medium Priority Issues:** 44
- **Low Priority Issues:** 6
- **Total Issues:** 687

## Detailed Findings

### Hardcoded Credential

**Severity:** CRITICAL
**File:** create_xss_user.py
**Line:** 6
**Description:** Hardcoded credentials found in source code
**Code:** `"password"`

---

**Severity:** CRITICAL
**File:** cultivar_app.py
**Line:** 110
**Description:** Hardcoded credentials found in source code
**Code:** `", 429

    # Create database tables and initialize data
    with app.app_context():
        try:
            from app.models import migrate_db, init_db
            from app.models.base_models import User
            from app.models.acinfinity_models import ACInfinityDevice, ACInfinityToken
            from app.models.ecowitt_models import EcowittDevice
            from app.models.system_models import SystemActivity
            from werkzeug.security import generate_password_hash
            
            # Create tables
            db.create_all()
            
            # Initialize default data
            init_db()
            
            
            # Create a test plant for clone demonstration if no plants exist
            from app.models.base_models import Plant, Strain, Status, Zone, Breeder
            if Plant.query.count() == 0:
                # Create a test breeder
                test_breeder = Breeder.query.filter_by(name='`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 3
**Description:** Hardcoded credentials found in source code
**Code:** `"

from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from app.logger import logger
from app.models import db
from app.models.base_models import User
from app.models.system_models import SystemActivity
from app.utils.validators import cleanse_user_data


def get_all_users():
    "`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 44
**Description:** Hardcoded credentials found in source code
**Code:** `"force_password_change"`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 62
**Description:** Hardcoded credentials found in source code
**Code:** `"
                    if not user.force_password_change
                    else "`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 107
**Description:** Hardcoded credentials found in source code
**Code:** `"force_password_change"`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 135
**Description:** Hardcoded credentials found in source code
**Code:** `"
    Create a new user.

    Args:
        data (dict): User data containing username, password, phone/email, and role info.

    Returns:
        dict: Result of the operation with success status and user ID.
    "`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 151
**Description:** Hardcoded credentials found in source code
**Code:** `")
        password = cleaned_data.get("`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 155
**Description:** Hardcoded credentials found in source code
**Code:** `", False)
        force_password_change = cleaned_data.get("`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 174
**Description:** Hardcoded credentials found in source code
**Code:** `"}

        # Create new user
        new_user = User(
            username=username,
            phone=phone,
            email=email,
            is_admin=is_admin,
            force_password_change=force_password_change,
        )
        new_user.password_hash = generate_password_hash(password)

        db.session.add(new_user)
        db.session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=new_user.id,
            type="`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 230
**Description:** Hardcoded credentials found in source code
**Code:** `", user.is_admin)
        user.force_password_change = data.get(
            "`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 232
**Description:** Hardcoded credentials found in source code
**Code:** `", user.force_password_change
        )
        user.updated_at = datetime.now()

        # Update password if provided
        new_password = data.get("`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 237
**Description:** Hardcoded credentials found in source code
**Code:** `")
        if new_password:
            user.password_hash = generate_password_hash(new_password)
            user.force_password_change = data.get("`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 360
**Description:** Hardcoded credentials found in source code
**Code:** `": str(e)}


def force_password_reset(user_id):
    "`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 364
**Description:** Hardcoded credentials found in source code
**Code:** `"
    Force a user to reset their password on next login.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Result of the operation.
    "`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 376
**Description:** Hardcoded credentials found in source code
**Code:** `"}

        user.force_password_change = True
        user.updated_at = datetime.now()

        db.session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=user.id,
            type="`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 387
**Description:** Hardcoded credentials found in source code
**Code:** `"Password reset forced for user: {user.username}"`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 395
**Description:** Hardcoded credentials found in source code
**Code:** `"Password reset forced for {user.username}"`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 399
**Description:** Hardcoded credentials found in source code
**Code:** `"Error forcing password reset: {e}"`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 409
**Description:** Hardcoded credentials found in source code
**Code:** `"
    try:
        total_users = User.query.count()
        admin_users = User.query.filter_by(is_admin=True).count()
        regular_users = total_users - admin_users
        users_needing_password_reset = User.query.filter_by(
            force_password_change=True
        ).count()

        # Recent user registrations (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_registrations = User.query.filter(
            User.created_at >= thirty_days_ago
        ).count()

        return {
            "`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 428
**Description:** Hardcoded credentials found in source code
**Code:** `"users_needing_password_reset"`

---

**Severity:** CRITICAL
**File:** app/handlers/user_handlers.py
**Line:** 437
**Description:** Hardcoded credentials found in source code
**Code:** `"users_needing_password_reset"`

---

**Severity:** CRITICAL
**File:** app/handlers/export_handlers.py
**Line:** 222
**Description:** Hardcoded credentials found in source code
**Code:** `"Force Password Change"`

---

**Severity:** CRITICAL
**File:** app/handlers/export_handlers.py
**Line:** 239
**Description:** Hardcoded credentials found in source code
**Code:** `"force_password_change"`

---

**Severity:** CRITICAL
**File:** app/handlers/settings_handlers.py
**Line:** 3
**Description:** Hardcoded credentials found in source code
**Code:** `"

import os

from werkzeug.utils import secure_filename

from app.config.config import Config
from app.logger import logger
from app.models import db
from app.models.base_models import Settings, User

# from app.utils.auth import hash_password # Make sure this line is commented out or removed
from app.utils.image import save_image


def get_settings():
    "`

---

**Severity:** CRITICAL
**File:** app/handlers/settings_handlers.py
**Line:** 155
**Description:** Hardcoded credentials found in source code
**Code:** `": str(e)}


def update_user_password(user_id, password):
    "`

---

**Severity:** CRITICAL
**File:** app/handlers/settings_handlers.py
**Line:** 160
**Description:** Hardcoded credentials found in source code
**Code:** `'s password.

    Args:
        user_id (int): The ID of the user.
        password (str): The new password.

    Returns:
        bool: True if successful, False otherwise.
    "`

---

**Severity:** CRITICAL
**File:** app/handlers/settings_handlers.py
**Line:** 168
**Description:** Hardcoded credentials found in source code
**Code:** `"
    try:
        user = db.session.get(User, user_id)

        if not user:
            return False

        # Update the user
        user.set_password(password)  # Use the User model'`

---

**Severity:** CRITICAL
**File:** app/handlers/settings_handlers.py
**Line:** 183
**Description:** Hardcoded credentials found in source code
**Code:** `"Error updating user password: {e}"`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 102
**Description:** Hardcoded credentials found in source code
**Code:** `"


def validate_password(password: str) -> Tuple[bool, str]:
    "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 106
**Description:** Hardcoded credentials found in source code
**Code:** `"
    Validate password strength requirements.

    Args:
        password (str): The password to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 114
**Description:** Hardcoded credentials found in source code
**Code:** `"
    if not password:
        return False, "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 116
**Description:** Hardcoded credentials found in source code
**Code:** `"

    if not isinstance(password, str):
        return False, "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 119
**Description:** Hardcoded credentials found in source code
**Code:** `"

    if len(password) < 8:
        return False, "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 122
**Description:** Hardcoded credentials found in source code
**Code:** `"

    if len(password) > 128:
        return False, "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 128
**Description:** Hardcoded credentials found in source code
**Code:** `', password):
        return False, "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 132
**Description:** Hardcoded credentials found in source code
**Code:** `', password):
        return False, "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 136
**Description:** Hardcoded credentials found in source code
**Code:** `', password):
        return False, "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 140
**Description:** Hardcoded credentials found in source code
**Code:** `', password):
        return False, "`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 237
**Description:** Hardcoded credentials found in source code
**Code:** `'].strip().lower()

    # Validate password (but don'`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 240
**Description:** Hardcoded credentials found in source code
**Code:** `'password'`

---

**Severity:** CRITICAL
**File:** app/utils/validators.py
**Line:** 241
**Description:** Hardcoded credentials found in source code
**Code:** `'password'`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 3
**Description:** Hardcoded credentials found in source code
**Code:** `"
import bcrypt

from app.logger import logger

# def hash_password(password): #commented out
#    "`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 9
**Description:** Hardcoded credentials found in source code
**Code:** `"
#    Hash a password using bcrypt.
#
#    Args:
#        password (str): The password to hash.
#
#    Returns:
#        str: The hashed password.
#    "`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 17
**Description:** Hardcoded credentials found in source code
**Code:** `"
#    try:
#        # Generate a salt and hash the password
#        password_bytes = password.encode('`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 20
**Description:** Hardcoded credentials found in source code
**Code:** `')
#        salt = bcrypt.gensalt()
#        hashed = bcrypt.hashpw(password_bytes, salt)
#        return hashed.decode('`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 25
**Description:** Hardcoded credentials found in source code
**Code:** `"Error hashing password: {e}"`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 30
**Description:** Hardcoded credentials found in source code
**Code:** `"
    Check if a password matches a hash.

    Args:
        password (str): The password to check.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    "`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 39
**Description:** Hardcoded credentials found in source code
**Code:** `"
    try:
        # Check if the password matches the hash
        password_bytes = password.encode("`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 42
**Description:** Hardcoded credentials found in source code
**Code:** `")
        hashed_bytes = hashed_password.encode("`

---

**Severity:** CRITICAL
**File:** app/utils/auth.py
**Line:** 43
**Description:** Hardcoded credentials found in source code
**Code:** `")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logger.error(f"`

---

**Severity:** CRITICAL
**File:** app/config/config.py
**Line:** 25
**Description:** Hardcoded credentials found in source code
**Code:** `")
    DB_PASSWORD = os.getenv("`

---

**Severity:** CRITICAL
**File:** app/config/config.py
**Line:** 70
**Description:** Hardcoded credentials found in source code
**Code:** `"acinfinity_password"`

---

**Severity:** CRITICAL
**File:** app/config/config.py
**Line:** 90
**Description:** Hardcoded credentials found in source code
**Code:** `"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"`

---

**Severity:** CRITICAL
**File:** app/config/config.py
**Line:** 118
**Description:** Hardcoded credentials found in source code
**Code:** `")
                if not cls.DB_PASSWORD:
                    raise ValueError("`

---

**Severity:** CRITICAL
**File:** app/routes/routes.py
**Line:** 3
**Description:** Hardcoded credentials found in source code
**Code:** `"

import os

from flask import (
    Flask,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_login import (
    current_user,  # Assuming Flask-Login is used/intended
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import (  # Added generate for potential future use
    check_password_hash,
    generate_password_hash,
)

from app.config.config import Config  # Corrected import path
from app.handlers import (
    breeder_handlers,
    plant_handlers,
    sensor_handlers,
    settings_handlers,
    strain_handlers,
)
from app.logger import logger  # Corrected import path for logger as well
from app.models.base_models import Plant, Sensor, Strain, Stream, User, db

# Removed: from utils.auth import check_password # Using werkzeug check_password_hash directly
from app.utils.helpers import format_date, format_datetime


def register_routes(app):
    "`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 3
**Description:** Hardcoded credentials found in source code
**Code:** `"

from datetime import datetime, timedelta
from io import BytesIO

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required

from app.handlers.export_handlers import (
    export_activities_csv,
    export_complete_backup,
    export_plants_csv,
    export_plants_json,
    export_sensors_csv,
    export_strains_csv,
    export_strains_json,
    export_users_csv,
    get_export_statistics,
)
from app.handlers.user_handlers import (
    create_user,
    delete_user,
    force_password_reset,
    get_all_users,
    get_user_by_id,
    get_user_statistics,
    toggle_user_admin_status,
    update_user,
)
from app.models import db
from app.models.base_models import User
from app.utils.rate_limiter import limiter
from app.models.base_models import User

admin_bp = Blueprint(
    "`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 82
**Description:** Hardcoded credentials found in source code
**Code:** `"password"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 82
**Description:** Hardcoded credentials found in source code
**Code:** `"password"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 86
**Description:** Hardcoded credentials found in source code
**Code:** `"force_password_change"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 86
**Description:** Hardcoded credentials found in source code
**Code:** `"force_password_change"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 119
**Description:** Hardcoded credentials found in source code
**Code:** `"force_password_change"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 119
**Description:** Hardcoded credentials found in source code
**Code:** `"force_password_change"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 119
**Description:** Hardcoded credentials found in source code
**Code:** `",
        }

        # Only update password if provided
        password = request.form.get("`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 123
**Description:** Hardcoded credentials found in source code
**Code:** `")
        if password:
            user_data["`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 125
**Description:** Hardcoded credentials found in source code
**Code:** `"] = password

        result = update_user(user_id, user_data)

        if result["`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 160
**Description:** Hardcoded credentials found in source code
**Code:** `"/users/<int:user_id>/force-password-reset"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 160
**Description:** Hardcoded credentials found in source code
**Code:** `"])
@login_required
def force_password_reset_route(user_id):
    "`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 163
**Description:** Hardcoded credentials found in source code
**Code:** `"Force password reset for a user."`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 165
**Description:** Hardcoded credentials found in source code
**Code:** `"})

    result = force_password_reset(user_id)
    return jsonify(result)


# API endpoints for AJAX requests
@admin_bp.route("`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 531
**Description:** Hardcoded credentials found in source code
**Code:** `"/api/users/<int:user_id>/reset-password"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 531
**Description:** Hardcoded credentials found in source code
**Code:** `"])
@admin_required
def reset_user_password_api(user_id):
    "`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 534
**Description:** Hardcoded credentials found in source code
**Code:** `'s password."`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 542
**Description:** Hardcoded credentials found in source code
**Code:** `"new_password"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 543
**Description:** Hardcoded credentials found in source code
**Code:** `"New password is required"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 546
**Description:** Hardcoded credentials found in source code
**Code:** `"new_password"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 546
**Description:** Hardcoded credentials found in source code
**Code:** `'s method

    # Set force_password_change flag if requested
    if data.get("`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 549
**Description:** Hardcoded credentials found in source code
**Code:** `"):
        user.force_password_change = True

    # Save changes
    db.session.commit()

    return jsonify({"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 555
**Description:** Hardcoded credentials found in source code
**Code:** `"Password reset successfully"`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 160
**Description:** Hardcoded credentials found in source code
**Code:** `admin_bp.route("/users/<int:user_id>/force-password-reset", methods=["POST"])
@login_required
def force_password_reset_route(user_id):
    "`

---

**Severity:** CRITICAL
**File:** app/blueprints/admin.py
**Line:** 531
**Description:** Hardcoded credentials found in source code
**Code:** `admin_bp.route("/api/users/<int:user_id>/reset-password", methods=["POST"])
@admin_required
def reset_user_password_api(user_id):
    "`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 3
**Description:** Hardcoded credentials found in source code
**Code:** `"

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.logger import logger
from app.models.base_models import User, db
from app.utils.rate_limiter import limiter

auth_bp = Blueprint("`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 28
**Description:** Hardcoded credentials found in source code
**Code:** `")
        password = request.form.get("`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 31
**Description:** Hardcoded credentials found in source code
**Code:** `"Password provided: {'`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 31
**Description:** Hardcoded credentials found in source code
**Code:** `' if password else '`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 33
**Description:** Hardcoded credentials found in source code
**Code:** `"LOGIN DEBUG: username={username}, password={'`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 33
**Description:** Hardcoded credentials found in source code
**Code:** `' if password else '`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 41
**Description:** Hardcoded credentials found in source code
**Code:** `"User has password_hash: {hasattr(user, '`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 43
**Description:** Hardcoded credentials found in source code
**Code:** `"Password hash exists: {bool(user.password_hash) if hasattr(user, '`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 46
**Description:** Hardcoded credentials found in source code
**Code:** `"LOGIN DEBUG: User has password_hash: {hasattr(user, '`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 49
**Description:** Hardcoded credentials found in source code
**Code:** `"password_hash"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 51
**Description:** Hardcoded credentials found in source code
**Code:** `"Password check result: {password_check}"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 52
**Description:** Hardcoded credentials found in source code
**Code:** `"LOGIN DEBUG: Password check result: {password_check}"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 54
**Description:** Hardcoded credentials found in source code
**Code:** `"User has no password_hash"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 55
**Description:** Hardcoded credentials found in source code
**Code:** `"LOGIN DEBUG: ERROR - User has no password_hash"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 59
**Description:** Hardcoded credentials found in source code
**Code:** `"password_hash"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 72
**Description:** Hardcoded credentials found in source code
**Code:** `"Invalid username or password."`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 73
**Description:** Hardcoded credentials found in source code
**Code:** `"Invalid username or password"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 87
**Description:** Hardcoded credentials found in source code
**Code:** `")
        password = request.form.get("`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 88
**Description:** Hardcoded credentials found in source code
**Code:** `")

        # Check required fields
        if not password:
            flash("`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 124
**Description:** Hardcoded credentials found in source code
**Code:** `"
            counter += 1

        # Create new user
        new_user = User(username=username)
        new_user.password_hash = generate_password_hash(password)

        if phone:
            new_user.phone = phone
        if email:
            new_user.email = email

        db.session.add(new_user)
        db.session.commit()

        flash(f"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 163
**Description:** Hardcoded credentials found in source code
**Code:** `"/forgot-password"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 163
**Description:** Hardcoded credentials found in source code
**Code:** `"])
def forgot_password():
    "`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 165
**Description:** Hardcoded credentials found in source code
**Code:** `"Handle password reset request (Placeholder)."`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 169
**Description:** Hardcoded credentials found in source code
**Code:** `"Forgot Password"`

---

**Severity:** CRITICAL
**File:** app/blueprints/auth.py
**Line:** 170
**Description:** Hardcoded credentials found in source code
**Code:** `"Forgot Password Page - Coming Soon!"`

---

**Severity:** CRITICAL
**File:** app/models/base_models.py
**Line:** 3
**Description:** Hardcoded credentials found in source code
**Code:** `"

from datetime import datetime

from flask_login import UserMixin
import bcrypt
from werkzeug.security import (
    check_password_hash,  # Import hashing functions
    generate_password_hash,
)

from app.models import db


class User(db.Model, UserMixin):
    "`

---

**Severity:** CRITICAL
**File:** app/models/base_models.py
**Line:** 18
**Description:** Hardcoded credentials found in source code
**Code:** `"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(
        db.String(128), nullable=False
    )  # Renamed to password_hash
    phone = db.Column(db.String(20))  # Phone number field
    email = db.Column(db.String(120))  # Email field
    force_password_change = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add is_admin field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def set_password(self, password):
        "`

---

**Severity:** CRITICAL
**File:** app/models/base_models.py
**Line:** 35
**Description:** Hardcoded credentials found in source code
**Code:** `"Hashes the password and sets the password_hash."`

---

**Severity:** CRITICAL
**File:** app/models/base_models.py
**Line:** 35
**Description:** Hardcoded credentials found in source code
**Code:** `"
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        "`

---

**Severity:** CRITICAL
**File:** app/models/base_models.py
**Line:** 39
**Description:** Hardcoded credentials found in source code
**Code:** `"Checks if the provided password matches the stored hash."`

---

**Severity:** CRITICAL
**File:** app/models/base_models.py
**Line:** 39
**Description:** Hardcoded credentials found in source code
**Code:** `"
        return check_password_hash(self.password_hash, password)


class PlantActivity(db.Model):
    "`

---

### Default Credentials in Documentation

**Severity:** HIGH
**File:** README.md
**Description:** Default admin credentials exposed in documentation

---

**Severity:** HIGH
**File:** plan.md
**Description:** Default admin credentials exposed in documentation

---

**Severity:** HIGH
**File:** audit_report.md
**Description:** Default admin credentials exposed in documentation

---

**Severity:** HIGH
**File:** docs/deployment_checklist.md
**Description:** Default admin credentials exposed in documentation

---

**Severity:** HIGH
**File:** docs/Wiki/User_Docs.md
**Description:** Default admin credentials exposed in documentation

---

### XSS Vulnerability

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 9
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/bootstrap.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 10
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/all.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 12
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/style.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 13
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/admin-fix.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 14
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='images/apple-touch-icon.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 15
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='images/favicon-32x32.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 16
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='images/favicon-16x16.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 336
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 346
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_users') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 383
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_logout') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 421
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_logout') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 435
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ category }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 436
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ message }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 461
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/jquery.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 462
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 463
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/chart.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/admin_base.html
**Line:** 489
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/admin-diagnostics.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 9
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/bootstrap.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 10
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/all.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 12
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/style.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 13
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='images/apple-touch-icon.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 14
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='images/favicon-32x32.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 15
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='images/favicon-16x16.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 41
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('market.cart') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 57
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ current_user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 60
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('market.cart') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 68
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.logout') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 79
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ category }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 80
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ message }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 98
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/jquery.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 99
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 101
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/chart.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 102
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/main.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/base.html
**Line:** 103
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/cart-utilities.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('dashboard.dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 17
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('dashboard.dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 23
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('dashboard.plants') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 29
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('strains.add_strain_page') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 36
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clones.dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 55
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('market.extensions') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 61
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('market.gear') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 85
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin.users') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 92
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin.export') }}`

---

**Severity:** HIGH
**File:** app/web/templates/common/sidebar.html
**Line:** 104
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ version }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 8
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 15
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clones_dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 17
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 29
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.grandparent.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 30
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.grandparent.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 47
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.parent.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 48
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.parent.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 49
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.parent.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 51
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.parent.start_date }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 56
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clone_lineage', clone_id=lineage.parent.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 80
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sibling.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 81
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sibling.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 83
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sibling.start_date }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 88
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clone_lineage', clone_id=sibling.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 100
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 101
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.plant.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 127
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ child.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 128
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ child.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 129
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ child.current_week }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 129
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ child.current_day }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 131
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ child.start_date }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 136
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clone_lineage', clone_id=child.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 178
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.siblings|length }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 188
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.children|length }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 198
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.plant.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 207
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('create_clone') }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 207
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ lineage.plant.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/lineage.html
**Line:** 213
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clones_dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 23
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone_stats.total_clones }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 34
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone_stats.successful_clones }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 45
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone_stats.success_rate }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 56
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone_stats.recent_clones }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 72
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 73
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 76
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.clone_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 80
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clone_lineage', clone_id=parent.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 93
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clones.create') }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 120
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 123
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 125
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.description }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 130
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clone_lineage', clone_id=clone.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 132
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.parent_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 135
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 138
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 140
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 142
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 144
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 146
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 148
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 152
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.days_alive }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 154
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.start_date }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 158
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.current_week }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 158
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.current_day }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 160
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.zone_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 163
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clone_lineage', clone_id=clone.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 169
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 170
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ clone.name|tojson }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/dashboard.html
**Line:** 187
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clones.create') }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 15
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clones_dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 30
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 31
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 32
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 33
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 35
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 37
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 38
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.breeder_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 41
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.status.lower() }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 41
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 42
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.current_week }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 42
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.current_day }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 43
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.clone_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 46
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ parent.description }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 61
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('plants') }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 105
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('clones_dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 493
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/clones/create.html
**Line:** 493
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 109
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.email_address|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 146
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 147
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.last_login|default('Never') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 157
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 157
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 157
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.active }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 160
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 160
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 164
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 164
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 338
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.polling_interval|default(60) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 354
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.data_retention|default(30) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 381
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.acinfinity_username|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 385
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.acinfinity_password|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 404
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_api_key|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 408
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_application_key|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 412
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_mac|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 495
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_time|default('02:00') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 499
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_retention|default(7) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 504
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_location|default('./backups') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_functional.html
**Line:** 606
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='img/logo.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/user_dashboard.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/user_dashboard.html
**Line:** 11
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/user_dashboard.html
**Line:** 40
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('sensors') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/user_dashboard.html
**Line:** 58
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('settings') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/graph.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/graph.html
**Line:** 11
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor_id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/graph.html
**Line:** 52
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor_id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 34
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plants|length if plants else 0 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 54
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ active_plants|length if active_plants else 0 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 74
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strains|length if strains else 0 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 94
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ harvested|length if harvested else 0 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 139
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 140
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.strain_name or 'Unknown' }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 142
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status|lower == 'active' ? 'success' : 'secondary' }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 143
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status or 'Unknown' }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 146
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.age or 0 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard.html
**Line:** 148
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 57
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.accent_color|default('#4CAF50') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 113
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.email_address|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 150
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 151
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.last_login|default('Never') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 161
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 161
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 161
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.active }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 164
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 164
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 168
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 168
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 342
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.polling_interval|default(60) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 358
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.data_retention|default(30) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 385
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.acinfinity_username|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 389
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.acinfinity_password|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 408
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_api_key|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 412
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_application_key|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 416
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_mac|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 499
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_time|default('02:00') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 503
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_retention|default(7) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 508
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_location|default('./backups') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings.html
**Line:** 610
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='img/logo.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 6
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 8
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/bootstrap.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 10
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/all.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 12
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/style.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 50
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 51
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ message }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 56
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ category if category else 'info' }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 57
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ message }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 64
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/auth_placeholder.html
**Line:** 70
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 27
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 27
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 67
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.type|lower }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 68
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.breeder_id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 69
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.autoflower|lower }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 72
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 91
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.breeder_name|default('Unknown') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 95
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.indica }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 95
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.sativa }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 99
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.cycle_time|default('Unknown') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 103
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.seed_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 108
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.short_description }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 113
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('strains.strain_detail', strain_id=strain.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 116
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 116
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 119
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 119
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 162
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 162
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 501
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/diagnostics.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strains.html
**Line:** 502
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/strains-diagnostics.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 16
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 16
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 60
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ total_sensors }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 73
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ active_sensors }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 86
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ warning_sensors }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 99
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ data_points }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 112
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 113
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 118
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor.type|lower }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 120
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 123
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor.latest_data.value }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 123
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor.unit }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 125
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor.latest_data.created_at|datetime }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 131
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('sensor', sensor_id=sensor.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 134
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 137
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 152
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 153
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 181
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 181
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 252
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/sensors.html
**Line:** 252
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/add_breeder.html
**Line:** 14
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('dashboard.dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 15
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 108
**Description:** Unescaped template variable - potential XSS
**Code:** `{{product_id}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 114
**Description:** Unescaped template variable - potential XSS
**Code:** `{{image}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 114
**Description:** Unescaped template variable - potential XSS
**Code:** `{{name}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 116
**Description:** Unescaped template variable - potential XSS
**Code:** `{{name}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 118
**Description:** Unescaped template variable - potential XSS
**Code:** `{{category}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 119
**Description:** Unescaped template variable - potential XSS
**Code:** `{{#if rating}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 121
**Description:** Unescaped template variable - potential XSS
**Code:** `{{rating}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 123
**Description:** Unescaped template variable - potential XSS
**Code:** `{{/if}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 131
**Description:** Unescaped template variable - potential XSS
**Code:** `{{quantity}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 137
**Description:** Unescaped template variable - potential XSS
**Code:** `{{unit_price.toFixed(2)}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/cart.html
**Line:** 138
**Description:** Unescaped template variable - potential XSS
**Code:** `{{total_price.toFixed(2)}}`

---

**Severity:** HIGH
**File:** app/web/templates/views/add_strain.html
**Line:** 14
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('dashboard.dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/add_strain.html
**Line:** 38
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/add_strain.html
**Line:** 38
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 19
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 34
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 49
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ sensor_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 64
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 88
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ python_version }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 92
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ flask_version }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 96
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ db_size_mb }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 100
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ os_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 100
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ os_version }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 108
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ uptime }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 183
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.plant }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 185
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.strain }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 187
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.sensor }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 187
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.value }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 189
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.new_user }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 194
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.user }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 195
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.timestamp.strftime('%Y-%m-%d %H:%M') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 328
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/admin-diagnostics.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 362
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/admin-diagnostics.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_dashboard.html
**Line:** 608
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/admin-diagnostics.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 7
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/bootstrap.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 8
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/all.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 9
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/style.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 57
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_logout') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 74
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ python_version }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 78
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ flask_version }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 82
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ db_size_mb }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 86
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ os_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 86
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ os_version }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 94
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ uptime }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 157
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/jquery.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 158
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 203
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/admin-diagnostics.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/simple_admin_dashboard.html
**Line:** 237
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/admin-diagnostics.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 57
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.accent_color|default('#4CAF50') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 113
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.email_address|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 150
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 151
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.last_login|default('Never') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 161
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 161
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 161
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.active }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 164
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 164
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 168
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 168
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 342
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.polling_interval|default(60) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 358
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.data_retention|default(30) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 385
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.acinfinity_username|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 389
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.acinfinity_password|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 408
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_api_key|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 412
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_application_key|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 416
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.ecowitt_mac|default('') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 499
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_time|default('02:00') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 503
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_retention|default(7) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 508
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ settings.backup_location|default('./backups') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/settings_old.html
**Line:** 610
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='img/logo.png') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard_mobile.html
**Line:** 8
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/dashboard-widgets.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard_mobile.html
**Line:** 14
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ current_user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard_mobile.html
**Line:** 87
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/dashboard-widgets.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/dashboard_mobile.html
**Line:** 221
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for("plants") }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/placeholder.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/placeholder.html
**Line:** 11
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/placeholder.html
**Line:** 14
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/placeholder.html
**Line:** 16
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('dashboard.dashboard') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 11
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 264
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.image_url }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 264
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 271
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 272
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status|lower }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 272
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 282
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 286
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 290
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.zone }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 294
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.age }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 298
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.start_date or 'Unknown' }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 302
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ 'Clone' if plant.is_clone else 'Seed' }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 311
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.current_week }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 315
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.current_day }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 320
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status|lower }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 320
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 329
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.description }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 353
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status|lower }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 356
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.start_date or 'Unknown' }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 370
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 380
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plant.html
**Line:** 390
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/index.html
**Line:** 8
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/dashboard-widgets.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/index.html
**Line:** 14
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ current_user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/index.html
**Line:** 76
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/dashboard-widgets.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/index.html
**Line:** 260
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for("dashboard.plants") }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_users.html
**Line:** 51
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_users.html
**Line:** 52
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_users.html
**Line:** 53
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.email }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_users.html
**Line:** 68
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.last_login|default('Never', true) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_users.html
**Line:** 70
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_users.html
**Line:** 73
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_users.html
**Line:** 76
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/new_login.html
**Line:** 8
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/bootstrap.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/new_login.html
**Line:** 10
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/all.min.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/new_login.html
**Line:** 12
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/style.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/new_login.html
**Line:** 32
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ category if category else 'info' }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/new_login.html
**Line:** 33
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ message }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/new_login.html
**Line:** 59
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.forgot_password') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/new_login.html
**Line:** 303
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 440
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ status_option }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 440
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ status_option }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 449
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain_option.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 449
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain_option.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 458
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone_option }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 458
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone_option }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 478
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plants|length }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 487
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plants|selectattr('status', 'equalto', 'Vegetative')|list|length }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 496
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plants|selectattr('status', 'equalto', 'Flowering')|list|length }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 505
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status|lower }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 506
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.zone }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 507
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.strain_id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 512
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.image_url }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 512
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 518
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status|lower }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 519
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.status }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 525
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 529
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.strain_name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 533
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.age }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 537
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.zone }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 543
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('plant', plant_id=plant.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 547
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 551
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 602
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain_option.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 602
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain_option.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 611
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone_option }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 611
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone_option }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 622
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ status_option }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 622
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ status_option }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 641
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant_option.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/plants.html
**Line:** 641
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ plant_option.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/admin_test.html
**Line:** 9
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 11
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 28
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 35
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.short_description }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 49
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.indica }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 49
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.sativa }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 53
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.cycle_time }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 57
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.seed_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 63
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.url }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 64
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.url }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 102
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ large_arc }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 102
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ end_x }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 102
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ end_y }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 115
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.indica }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 119
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.sativa }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 132
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.description }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 180
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 185
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 191
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 192
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ breeder.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 199
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.short_description }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 203
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.cycle_time }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 224
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.indica }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 226
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.indica }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 227
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.sativa }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 232
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.seed_count }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 236
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.url }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 242
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.description }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 265
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 318
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.indica }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 318
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.sativa }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 396
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ strain.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 460
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/strain.html
**Line:** 460
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ zone.name }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 16
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='css/landing.css') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 19
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='manifest.json') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 34
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 55
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 282
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 315
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 346
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 403
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 474
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('auth.login') }}`

---

**Severity:** HIGH
**File:** app/web/templates/landing/index.html
**Line:** 505
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='js/landing.js') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 7
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 15
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_users') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 29
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.username }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 52
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.phone or '' }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 61
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.email or '' }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 101
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.created_at }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 105
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.updated_at }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 109
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.recent_activities|length }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 119
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.type }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 120
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.description }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 121
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ activity.timestamp }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/edit_user.html
**Line:** 133
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_users') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 23
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.total_plants }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 25
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.living_plants }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 25
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.harvested_plants }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 34
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.total_strains }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 36
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.in_stock_strains }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 36
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.out_of_stock_strains }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 45
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.total_activities }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 56
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.total_sensors }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 58
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ export_stats.total_sensor_readings }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 77
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('export_plants', format='csv') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 80
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('export_plants', format='json') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 94
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('export_strains', format='csv') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 97
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('export_strains', format='json') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 111
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('export_activities') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 125
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('export_sensors') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 139
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('export_users') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/export.html
**Line:** 170
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('export_complete') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/create_user.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/create_user.html
**Line:** 15
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_users') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/create_user.html
**Line:** 96
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin_users') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 3
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ title }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 21
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user_stats.total_users }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 31
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user_stats.admin_users }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 41
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user_stats.regular_users }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 51
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user_stats.users_needing_password_reset }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 59
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin.create_user_route') }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 83
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 124
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.created_at }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 128
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.last_activity }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 135
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('admin.edit_user', user_id=user.id) }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 142
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 153
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/admin/users.html
**Line:** 160
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ user.id }}`

---

**Severity:** HIGH
**File:** app/web/templates/auth/change_password.html
**Line:** 9
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('static', filename='images/logo.svg') }}`

---

**Severity:** HIGH
**File:** app/web/templates/auth/change_password.html
**Line:** 18
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ category }}`

---

**Severity:** HIGH
**File:** app/web/templates/auth/change_password.html
**Line:** 19
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ message }}`

---

**Severity:** HIGH
**File:** app/web/templates/auth/change_password.html
**Line:** 28
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ url_for('change_password') }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 201
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ (i % 3) + 1 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 203
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ ['Mephisto Genetics', 'Barney\'s Farm', 'Dutch Passion'][i % 3] }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 204
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 204
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 206
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 215
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i * 10 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 217
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ 35 + i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 220
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i + 3 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 220
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/seed_bank.html
**Line:** 220
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ 35 + i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 207
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ (i % 3) + 1 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 209
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ ['AC Infinity', 'Spider Farmer', 'Fox Farm'][i % 3] }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 210
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 210
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 212
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 216
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 223
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i * 12 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 225
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ 29.99 + (i * 10) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 228
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i + 3 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 228
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/gear.html
**Line:** 228
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ 29.99 + (i * 10) }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/extensions.html
**Line:** 208
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/extensions.html
**Line:** 208
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/extensions.html
**Line:** 210
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/extensions.html
**Line:** 211
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/extensions.html
**Line:** 212
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/extensions.html
**Line:** 219
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ i * 10 }}`

---

**Severity:** HIGH
**File:** app/web/templates/views/market/extensions.html
**Line:** 221
**Description:** Unescaped template variable - potential XSS
**Code:** `{{ 19 + i }}`

---

### File Upload Security

**Severity:** HIGH
**File:** app/handlers/plant_handlers.py
**Description:** File upload without proper type validation

---

**Severity:** HIGH
**File:** app/handlers/settings_handlers.py
**Description:** File upload without proper type validation

---

**Severity:** HIGH
**File:** app/utils/image.py
**Description:** File upload without proper type validation

---

**Severity:** HIGH
**File:** app/config/config.py
**Description:** File upload without proper type validation

---

**Severity:** HIGH
**File:** app/routes/routes.py
**Description:** File upload without proper type validation

---

**Severity:** HIGH
**File:** app/watcher/watcher.py
**Description:** File upload without proper type validation

---

**Severity:** MEDIUM
**File:** app/handlers/plant_handlers.py
**Description:** File upload without size limits

---

**Severity:** MEDIUM
**File:** app/handlers/settings_handlers.py
**Description:** File upload without size limits

---

**Severity:** MEDIUM
**File:** app/utils/image.py
**Description:** File upload without size limits

---

**Severity:** MEDIUM
**File:** app/routes/routes.py
**Description:** File upload without size limits

---

**Severity:** MEDIUM
**File:** app/watcher/watcher.py
**Description:** File upload without size limits

---

### CSRF Protection

**Severity:** HIGH
**File:** global
**Description:** No CSRF protection mechanism found

---

**Severity:** MEDIUM
**File:** app/web/templates/signup.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/clones/create.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/sensors_standalone.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/settings_functional.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/settings_standalone_new.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/settings.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/strains.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/sensors.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/sensors_tab_standalone.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/add_breeder.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/add_strain.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/settings_old.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/settings_standalone.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/admin_users.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/new_login.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/plants.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/views/strain.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/landing/index.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/admin/edit_user.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/admin/create_user.html
**Description:** Form without CSRF token

---

**Severity:** MEDIUM
**File:** app/web/templates/auth/change_password.html
**Description:** Form without CSRF token

---

### Session Security

**Severity:** MEDIUM
**File:** app/config/config.py
**Description:** Secure cookies not enforced

---

**Severity:** MEDIUM
**File:** app/config/config.py
**Description:** HTTPOnly cookies not enforced

---

**Severity:** MEDIUM
**File:** app/config/config.py
**Description:** SameSite cookies not configured

---

**Severity:** MEDIUM
**File:** app/config/config.py
**Description:** Session timeout not configured

---

### Missing Authorization

**Severity:** MEDIUM
**File:** app/routes/routes.py
**Line:** 67
**Description:** Route without authentication requirement
**Code:** `@app.route("/")`

---

**Severity:** MEDIUM
**File:** app/routes/routes.py
**Line:** 72
**Description:** Route without authentication requirement
**Code:** `@app.route("/home")`

---

**Severity:** MEDIUM
**File:** app/routes/routes.py
**Line:** 77
**Description:** Route without authentication requirement
**Code:** `@app.route("/api/newsletter/subscribe", methods=["POST"])`

---

**Severity:** MEDIUM
**File:** app/routes/routes.py
**Line:** 109
**Description:** Route without authentication requirement
**Code:** `@app.route("/favicon.ico")`

---

**Severity:** MEDIUM
**File:** app/routes/routes.py
**Line:** 118
**Description:** Route without authentication requirement
**Code:** `@app.route("/manifest.json")`

---

**Severity:** MEDIUM
**File:** app/blueprints/admin.py
**Line:** 669
**Description:** Route without authentication requirement
**Code:** `@admin_bp.route("/api/diagnostics/test", methods=["GET"])`

---

**Severity:** MEDIUM
**File:** app/blueprints/diagnostics.py
**Line:** 15
**Description:** Route without authentication requirement
**Code:** `@diagnostics_bp.route("/diagnostics")`

---

**Severity:** MEDIUM
**File:** app/blueprints/auth.py
**Line:** 163
**Description:** Route without authentication requirement
**Code:** `@auth_bp.route("/forgot-password", methods=["GET", "POST"])`

---

### Information Disclosure

**Severity:** MEDIUM
**File:** dashboard.py
**Line:** 52
**Description:** Debug mode enabled - potential information disclosure

---

**Severity:** MEDIUM
**File:** main.py
**Line:** 33
**Description:** Debug mode enabled - potential information disclosure

---

**Severity:** MEDIUM
**File:** minimal_flask_test.py
**Line:** 15
**Description:** Debug mode enabled - potential information disclosure

---

**Severity:** MEDIUM
**File:** no_login_app.py
**Line:** 18
**Description:** Debug mode enabled - potential information disclosure

---

**Severity:** MEDIUM
**File:** test.py
**Line:** 10
**Description:** Debug mode enabled - potential information disclosure

---

**Severity:** MEDIUM
**File:** hello.py
**Line:** 7
**Description:** Debug mode enabled - potential information disclosure

---

**Severity:** LOW
**File:** test_talisman_simple.py
**Line:** 98
**Description:** Print statement with potential sensitive data
**Code:** `print("\n✅ All key security headers are present!")`

---

**Severity:** LOW
**File:** inspect_server.py
**Line:** 64
**Description:** Print statement with potential sensitive data
**Code:** `print("\n🏠 OTHER KEY ROUTES:")`

---

**Severity:** LOW
**File:** app/blueprints/auth.py
**Line:** 32
**Description:** Print statement with potential sensitive data
**Code:** `print(
            f"LOGIN DEBUG: username={username}, password={'***' if password else 'None'}"
        )`

---

**Severity:** LOW
**File:** app/blueprints/auth.py
**Line:** 45
**Description:** Print statement with potential sensitive data
**Code:** `print(
                f"LOGIN DEBUG: User has password_hash: {hasattr(user, 'password_hash')`

---

**Severity:** LOW
**File:** app/blueprints/auth.py
**Line:** 52
**Description:** Print statement with potential sensitive data
**Code:** `print(f"LOGIN DEBUG: Password check result: {password_check}")`

---

**Severity:** LOW
**File:** app/blueprints/auth.py
**Line:** 55
**Description:** Print statement with potential sensitive data
**Code:** `print("LOGIN DEBUG: ERROR - User has no password_hash")`

---

## Recommended Actions

### Immediate Actions (Critical/High)

1. **Hardcoded Credential** in `create_xss_user.py`: Hardcoded credentials found in source code
2. **Hardcoded Credential** in `cultivar_app.py`: Hardcoded credentials found in source code
3. **Hardcoded Credential** in `app/handlers/user_handlers.py`: Hardcoded credentials found in source code
4. **Hardcoded Credential** in `app/handlers/user_handlers.py`: Hardcoded credentials found in source code
5. **Hardcoded Credential** in `app/handlers/user_handlers.py`: Hardcoded credentials found in source code
6. **Hardcoded Credential** in `app/handlers/user_handlers.py`: Hardcoded credentials found in source code
7. **Hardcoded Credential** in `app/handlers/user_handlers.py`: Hardcoded credentials found in source code
8. **Hardcoded Credential** in `app/handlers/user_handlers.py`: Hardcoded credentials found in source code
9. **Hardcoded Credential** in `app/handlers/user_handlers.py`: Hardcoded credentials found in source code
10. **Hardcoded Credential** in `app/handlers/user_handlers.py`: Hardcoded credentials found in source code

### Next Steps (Medium/Low)

- Implement comprehensive input validation across all endpoints
- Add CSRF protection to all forms
- Configure secure session settings
- Regular dependency vulnerability scanning
- Code review processes for security
