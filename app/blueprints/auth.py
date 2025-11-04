"""
Authentication blueprint for the CultivAR application - ASYNC VERSION.
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.logger import logger
from app.models_async.auth import User
from app.models_async.system import SystemActivity
from app.utils.async_flask_helpers import FlaskAsyncSessionManager
from app.utils.rate_limiter import limiter

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="../web/templates")


@limiter.limit("5 per minute")
@auth_bp.route("/login", methods=["GET", "POST"])
async def login():
    """Handle user login."""
    logger.info(f"=== LOGIN ROUTE HIT ({request.method}) ===")
    print(f"=== LOGIN ROUTE DEBUG ({request.method}) ===")

    if current_user.is_authenticated:
        logger.info("User already authenticated. Redirecting to dashboard.")
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        logger.info(f"Login attempt for username: {username}")
        logger.info(f"Password provided: {'Yes' if password else 'No'}")
        print(
            f"LOGIN DEBUG: username={username}, password={'***' if password else 'None'}"
        )

        # Use async database session with Flask async helper
        async with FlaskAsyncSessionManager() as session:
            # Do async query directly
            user_result = await session.execute(select(User).where(User.username == username))
            user = user_result.scalars().first()
                
            logger.info(f"User found in database: {'Yes' if user else 'No'}")
            print(f"LOGIN DEBUG: User found: {'Yes' if user else 'No'}")

            if user:
                logger.info(f"User has password_hash: {hasattr(user, 'password_hash')}")
                logger.info(
                    f"Password hash exists: {bool(user.password_hash) if hasattr(user, 'password_hash') else False}"
                )
                print(
                    f"LOGIN DEBUG: User has password_hash: {hasattr(user, 'password_hash')}"
                )

                if hasattr(user, "password_hash") and user.password_hash:
                    password_check = check_password_hash(user.password_hash or "", password)
                    logger.info(f"Password check result: {password_check}")
                    print(f"LOGIN DEBUG: Password check result: {password_check}")
                else:
                    logger.error("User has no password_hash")
                    print("LOGIN DEBUG: ERROR - User has no password_hash")

            if (
                user
                and hasattr(user, "password_hash")
                and user.password_hash
                and user.password_hash is not None
                and check_password_hash(user.password_hash, password)
            ):
                logger.info("Login successful.")
                # Clear existing Flask session and regenerate to prevent session fixation attacks
                from flask import session as flask_session
                flask_session.clear()
                login_user(user)  # Log the user in
                logger.info("Session cleared and regenerated after login.")
                flash("Login successful!", "success")
                # Redirect to the page the user was trying to access, or dashboard
                next_page = request.args.get("next")
                return redirect(next_page or url_for("dashboard.dashboard"))
            else:
                logger.warning("Invalid username or password.")
                flash("Invalid username or password", "danger")
                return redirect(url_for("auth.login"))

    return render_template(
        "views/new_login.html", admin_login=False, title="User Login"
    )


@limiter.limit("2 per minute")
@auth_bp.route("/signup", methods=["GET", "POST"])
async def signup():
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
            if not email or "@" not in email:
                flash("Valid email address is required.", "danger")
                return render_template("signup.html", title="Sign Up")
            username = f"user_{email.split('@')[0]}"

        try:
            async with FlaskAsyncSessionManager() as session:
                # Check if user already exists by contact method
                existing_user = None
                if phone:
                    existing_result = await session.execute(select(User).where(User.phone == phone))
                    existing_user = existing_result.scalars().first()
                else:
                    existing_result = await session.execute(select(User).where(User.email == email))
                    existing_user = existing_result.scalars().first()

                if existing_user:
                    contact_type = "phone number" if phone else "email address"
                    flash(f"An account with this {contact_type} already exists.", "danger")
                    return render_template("signup.html", title="Sign Up")

                # Ensure username is unique
                counter = 1
                original_username = username
                while True:
                    username_check_result = await session.execute(select(User).where(User.username == username))
                    existing_username = username_check_result.scalars().first()
                    if not existing_username:
                        break
                    username = f"{original_username}_{counter}"
                    counter += 1

                # Create new user
                new_user = User(username=username)
                new_user.password_hash = generate_password_hash(password)

                if phone:
                    new_user.phone = phone
                if email:
                    new_user.email = email

                session.add(new_user)
                await session.commit()
                logger.info("User created successfully.")

        except Exception as e:
            logger.error(f"Error creating user: {e}")
            flash("Error creating account.", "danger")
            return render_template("signup.html", title="Sign Up")

        flash(f"Account created successfully! Your username is: {username}", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html", title="Sign Up")


@auth_bp.route("/logout")
@login_required
async def logout():
    """Handle user logout."""
    logger.info("=== LOGOUT ROUTE HIT ===")
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
async def forgot_password():
    """Handle password reset request (Placeholder)."""
    if request.method == "POST":
        # TODO: Implement actual password reset logic using async handlers
        flash("Password reset functionality coming soon.", "info")
        return redirect(url_for("auth.login"))
    
    # Render the auth placeholder template
    return render_template(
        "views/auth_placeholder.html",
        title="Forgot Password",
        message="Forgot Password Page - Coming Soon!",
    )
