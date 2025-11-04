"""
Newsletter blueprint for the CultivAR application - ASYNC VERSION.
Handles enhanced newsletter subscription and management.
"""

import re
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from sqlalchemy import or_, select

from app.logger import logger
from app.models_async.marketing import NewsletterSubscriber
from app.utils.async_flask_helpers import FlaskAsyncSessionManager
from app.utils.rate_limiter import limiter

newsletter_bp = Blueprint("newsletter", __name__, url_prefix="/newsletter", template_folder="../web/templates")


def is_valid_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """Validate phone number format (US format)."""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)

    # Check if it's a valid 10 or 11 digit number
    return len(digits) == 10 or len(digits) == 11


@newsletter_bp.route("/subscribe", methods=["GET", "POST"])
async def subscribe():
    """Handle newsletter subscriptions."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        subscription_type = request.form.get("subscription_type", "both")
        source = request.form.get("source", "newsletter_page")

        # Validate input
        has_email = bool(email)
        has_phone = bool(phone)

        if not has_email and not has_phone:
            flash("Please provide either an email address or phone number.", "danger")
            return redirect(url_for("newsletter.subscribe"))

        if has_email and not is_valid_email(email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("newsletter.subscribe"))

        if has_phone and not is_valid_phone(phone):
            flash("Please enter a valid phone number.", "danger")
            return redirect(url_for("newsletter.subscribe"))

        # Use Flask async session manager for proper Flask integration
        async with FlaskAsyncSessionManager() as session:
            # Check for existing subscriptions
            existing_subscriber = None

            if has_email:
                result = await session.execute(select(NewsletterSubscriber).where(NewsletterSubscriber.email == email))
                existing_subscriber = result.scalars().first()

            if has_phone and not existing_subscriber:
                result = await session.execute(select(NewsletterSubscriber).where(NewsletterSubscriber.phone == phone))
                existing_subscriber = result.scalars().first()

            if existing_subscriber:
                if existing_subscriber.is_active:
                    flash("You're already subscribed to our newsletter!", "info")
                else:
                    # Reactivate subscription
                    existing_subscriber.is_active = True
                    existing_subscriber.subscription_date = datetime.utcnow()
                    existing_subscriber.unsubscribe_date = None
                    await session.commit()
                    flash("Welcome back! Your subscription has been reactivated.", "success")
                return redirect(url_for("newsletter.subscribe"))

            # Create new subscription
            subscriber = NewsletterSubscriber(
                email=email if has_email else None,
                phone=phone if has_phone else None,
                subscription_type=subscription_type,
                ip_address=request.remote_addr,
                source=source
            )

            session.add(subscriber)
            await session.commit()

            logger.info(f"New newsletter subscription: {email or phone} (type: {subscription_type})")

            flash("Successfully subscribed to our newsletter! Check your email for confirmation.", "success")
            return redirect(url_for("newsletter.success"))

    return render_template("newsletter/subscribe.html", title="Newsletter Signup")


@newsletter_bp.route("/success")
def success():
    """Show subscription success page."""
    return render_template("newsletter/success.html", title="Subscription Confirmed")


@newsletter_bp.route("/unsubscribe", methods=["GET", "POST"])
async def unsubscribe():
    """Handle newsletter unsubscriptions."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        if not email and not phone:
            flash("Please provide an email address or phone number.", "danger")
            return redirect(url_for("newsletter.unsubscribe"))

        # Use Flask async session manager for proper Flask integration
        async with FlaskAsyncSessionManager() as session:
            # Find subscriber
            subscriber = None

            if email:
                result = await session.execute(
                    select(NewsletterSubscriber).where(
                        NewsletterSubscriber.email == email,
                        NewsletterSubscriber.is_active == True
                    )
                )
                subscriber = result.scalars().first()

            if phone and not subscriber:
                result = await session.execute(
                    select(NewsletterSubscriber).where(
                        NewsletterSubscriber.phone == phone,
                        NewsletterSubscriber.is_active == True
                    )
                )
                subscriber = result.scalars().first()

            if not subscriber:
                flash("No active subscription found with that information.", "warning")
                return redirect(url_for("newsletter.unsubscribe"))

            # Unsubscribe
            subscriber.is_active = False
            subscriber.unsubscribe_date = datetime.utcnow()
            await session.commit()

            logger.info(f"Newsletter unsubscription: {email or phone}")

            flash("Successfully unsubscribed from our newsletter.", "success")
            return redirect(url_for("newsletter.unsubscribe"))

    return render_template("newsletter/unsubscribe.html", title="Unsubscribe")


@newsletter_bp.route("/preferences", methods=["GET", "POST"])
async def preferences():
    """Handle subscription preferences."""
    email = request.args.get("email", "").strip().lower()

    if not email:
        flash("Email address required.", "danger")
        return redirect(url_for("newsletter.subscribe"))

    async with FlaskAsyncSessionManager() as session:
        result = await session.execute(
            select(NewsletterSubscriber).where(
                NewsletterSubscriber.email == email,
                NewsletterSubscriber.is_active == True
            )
        )
        subscriber = result.scalars().first()

        if not subscriber:
            flash("No active subscription found.", "warning")
            return redirect(url_for("newsletter.subscribe"))

        if request.method == "POST":
            subscription_type = request.form.get("subscription_type", "both")

            subscriber.subscription_type = subscription_type
            await session.commit()

            flash("Preferences updated successfully!", "success")
            return redirect(url_for("newsletter.preferences", email=email))

        return render_template(
            "newsletter/preferences.html",
            title="Newsletter Preferences",
            subscriber=subscriber
        )


# API Routes
@newsletter_bp.route("/api/subscribe", methods=["POST"])
async def api_subscribe():
    """API endpoint for newsletter subscription."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        email = data.get("email", "").strip().lower()
        phone = data.get("phone", "").strip()
        subscription_type = data.get("subscription_type", "both")
        source = data.get("source", "api")

        # Validate input
        has_email = bool(email)
        has_phone = bool(phone)

        if not has_email and not has_phone:
            return jsonify({"error": "Email or phone required"}), 400

        if has_email and not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        if has_phone and not is_valid_phone(phone):
            return jsonify({"error": "Invalid phone format"}), 400

        # Use async database session
        async with FlaskAsyncSessionManager() as session:
            # Check for existing subscription
            existing_subscriber = None

            if has_email:
                result = await session.execute(select(NewsletterSubscriber).where(NewsletterSubscriber.email == email))
                existing_subscriber = result.scalars().first()

            if has_phone and not existing_subscriber:
                result = await session.execute(select(NewsletterSubscriber).where(NewsletterSubscriber.phone == phone))
                existing_subscriber = result.scalars().first()

            if existing_subscriber and existing_subscriber.is_active:
                return jsonify({"message": "Already subscribed", "status": "existing"}), 200

            # Create or reactivate subscription
            if existing_subscriber:
                # Reactivate
                existing_subscriber.is_active = True
                existing_subscriber.subscription_date = datetime.utcnow()
                existing_subscriber.unsubscribe_date = None
                existing_subscriber.subscription_type = subscription_type
                status = "reactivated"
            else:
                # Create new
                subscriber = NewsletterSubscriber(
                    email=email if has_email else None,
                    phone=phone if has_phone else None,
                    subscription_type=subscription_type,
                    ip_address=request.remote_addr,
                    source=source
                )
                session.add(subscriber)
                status = "new"

            await session.commit()

            logger.info(f"Newsletter API subscription: {email or phone} (status: {status})")

            return jsonify({
                "message": "Successfully subscribed to newsletter",
                "status": status,
                "subscription_type": subscription_type
            }), 200

    except Exception as e:
        logger.error(f"Newsletter API error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@newsletter_bp.route("/api/stats")
async def api_stats():
    """Get newsletter statistics."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get total active subscribers
            total_result = await session.execute(
                select(NewsletterSubscriber).where(NewsletterSubscriber.is_active == True)
            )
            total_subscribers = len(total_result.scalars().all())

            # Get today's subscriptions
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
            today_result = await session.execute(
                select(NewsletterSubscriber).where(
                    NewsletterSubscriber.is_active == True,
                    NewsletterSubscriber.subscription_date >= today_start
                )
            )
            today_subscriptions = len(today_result.scalars().all())

            # Get total unsubscriptions
            unsub_result = await session.execute(
                select(NewsletterSubscriber).where(
                    NewsletterSubscriber.unsubscribe_date.isnot(None)
                )
            )
            unsubscriptions = len(unsub_result.scalars().all())

            active_rate = (total_subscribers / (total_subscribers + unsubscriptions)) * 100 if (total_subscribers + unsubscriptions) > 0 else 0

        return jsonify({
            "total_subscribers": total_subscribers,
            "today_subscriptions": today_subscriptions,
            "total_unsubscriptions": unsubscriptions,
            "active_rate": active_rate
        })

    except Exception as e:
        logger.error(f"Newsletter stats error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# Error Handlers
@newsletter_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("newsletter/404.html", title="Page Not Found"), 404


@newsletter_bp.errorhandler(500)
async def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Newsletter blueprint error: {error}")
    return render_template("newsletter/500.html", title="Server Error"), 500
