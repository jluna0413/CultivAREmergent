"""
Authentication blueprint for the CultivAR application.
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.logger import logger
from app.models.base_models import User, db
from app.utils.rate_limiter import limiter

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="../web/templates")


@limiter.limit("5 per minute")
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    logger.info(f"Login route accessed via {request.method}")

    if current_user.is_authenticated:
        logger.info("User already authenticated. Redirecting to dashboard.")
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        logger.info(f"Login attempt for username: {username}")

        # Use generic error message to prevent user enumeration
        generic_error = "Invalid username or password"

        user = User.query.filter_by(username=username).first()

        if (
            user
            and hasattr(user, "password_hash")
            and user.password_hash
            and check_password_hash(user.password_hash, password)
        ):
            logger.info("Login successful.")
            # Clear existing session and regenerate to prevent session fixation attacks
            session.clear()
            login_user(user)  # Log the user in
            logger.info("Session cleared and regenerated after login.")
            flash("Login successful!", "success")
            # Redirect to the page the user was trying to access, or dashboard
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.dashboard"))
        else:
            logger.warning("Invalid login attempt.")
            flash(generic_error, "danger")
            return redirect(url_for("auth.login"))

    return render_template(
        "views/new_login.html", admin_login=False, title="User Login"
    )


@limiter.limit("2 per minute")
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup."""
    if request.method == "POST":
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check required fields
        if not password:
            flash("Password is required.", "danger")
            return render_template("signup.html", title="Sign Up")

        # Check that either phone or email is provided
        if not phone and not email:
            flash("Either phone number or email address is required.", "danger")
            return render_template("signup.html", title="Sign Up")

        # Generate username from phone or email
        if phone:
            username = (
                f"user_{phone.replace('+', '').replace('-', '').replace(' ', '')}"
            )
        else:
            username = f"user_{email.split('@')[0]}"

        # Check if user already exists by contact method
        existing_user = None
        if phone:
            existing_user = User.query.filter_by(phone=phone).first()
        else:
            existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            contact_type = "phone number" if phone else "email address"
            flash(f"An account with this {contact_type} already exists.", "danger")
            return render_template("signup.html", title="Sign Up")

        # Ensure username is unique
        counter = 1
        original_username = username
        while User.query.filter_by(username=username).first():
            username = f"{original_username}_{counter}"
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

        flash(f"Account created successfully! Your username is: {username}", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html", title="Sign Up")


@auth_bp.route("/logout")
@login_required
def logout():
    """Handle user logout."""
    logger.info("User logout initiated")
    try:
        logout_user()
        # Clear session to prevent session fixation and ensure clean logout
        session.clear()
        logger.info("Session cleared after logout.")
        flash("You have been logged out successfully.", "success")
        return redirect(url_for("auth.login"))
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return "Internal Server Error", 500


@limiter.limit("1 per minute")
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Handle password reset request (Placeholder)."""
    # Render the auth placeholder template
    return render_template(
        "views/auth_placeholder.html",
        title="Forgot Password",
        message="Forgot Password Page - Coming Soon!",
    )
