"""
Marketing blueprint for the CultivAR application - ASYNC VERSION.
Handles waitlist, blog, and lead magnet functionality.
"""

import os
import secrets
import re
from datetime import datetime, timedelta
import traceback
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.utils.async_flask_helpers import FlaskAsyncSessionManager
try:
    # Prefer the external validator when available for stricter checks
    from email_validator import validate_email, EmailNotValidError  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    validate_email = None  # type: ignore
    EmailNotValidError = None  # type: ignore

# Import async handlers
from app.handlers.marketing_handlers_async import (
    create_waitlist_entry,
    get_waitlist_statistics,
    get_all_blog_posts,
    get_blog_post_by_slug,
    search_blog_posts,
    get_blog_categories,
    get_lead_magnet_by_name,
    has_recent_download,
    record_download_and_increment,
    subscribe_newsletter
)

marketing_bp = Blueprint("marketing", __name__, url_prefix="/marketing", template_folder="../web/templates")


def _validate_email_address(email: str) -> bool:
    """Validate an email using email_validator if available, else a regex.

    Returns True when valid, False otherwise.
    """
    if not email:
        return False

    if validate_email is not None:
        try:
            validate_email(email)
            return True
        except Exception as exc:  # narrow where possible; EmailNotValidError when available
            # If the library provides a specific exception class, treat it as expected validation failure
            if EmailNotValidError is not None and isinstance(exc, EmailNotValidError):
                return False
            return False

    # fallback regex
    email_re_local = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    return bool(email_re_local.match(email))


def _serve_lead_magnet_file(magnet: dict, magnet_name: str):
    """Return a Flask response for the magnet file or raise OSError if not found."""
    safe_dir = current_app.config.get('LEAD_MAGNET_DIR', os.path.join(current_app.root_path, 'static', 'lead_magnets'))
    safe_dir_abs = os.path.abspath(safe_dir)
    filename = os.path.basename(magnet['file_path'])
    file_path = os.path.join(safe_dir_abs, filename)

    if not os.path.exists(file_path):
        raise OSError(f"Lead magnet file not found: {file_path}")

    return send_from_directory(safe_dir_abs, filename, as_attachment=True, download_name=f"{secure_filename(magnet_name)}.pdf")


# Waitlist Routes
@marketing_bp.route("/waitlist", methods=["GET", "POST"])
async def waitlist():
    """Handle waitlist signups."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        priority_tier = request.form.get("priority_tier", "general")
        referral_code = request.form.get("referral_code", "").strip()

        # Validate email
        email_re = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
        if not email or not email_re.match(email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("marketing.waitlist"))

        # Generate referral code
        new_referral_code = secrets.token_urlsafe(8)

        try:
            async with FlaskAsyncSessionManager() as session:
                # Use async handler for waitlist creation
                result = await create_waitlist_entry(
                    email=email,
                    priority_tier=priority_tier,
                    referral_code=new_referral_code,
                    session=session
                )
                
                if result["success"]:
                    flash("Welcome to the waitlist! Check your email for next steps.", "success")
                    return redirect(url_for("marketing.waitlist_success", code=new_referral_code))
                else:
                    flash(result.get("error", "Failed to join waitlist. Please try again."), "danger")
                    return redirect(url_for("marketing.waitlist"))
        except Exception as e:
            logger.exception(f"Error creating waitlist entry: {e}")
            flash("An error occurred. Please try again later.", "danger")
            return redirect(url_for("marketing.waitlist"))

    return render_template("marketing/waitlist.html", title="Join the Waitlist")


@marketing_bp.route("/waitlist/success/<code>")
async def waitlist_success(code):
    """Show waitlist success page with referral code."""
    # Get email from form data if available, otherwise use placeholder
    email = request.form.get("email", "") if request.form else "user@example.com"
    return render_template(
        "marketing/waitlist_success.html",
        title="Welcome to the Waitlist",
        referral_code=code,
        email=email
    )


# Blog Routes
@marketing_bp.route("/blog")
async def blog():
    """Display blog posts."""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)

    try:
        async with FlaskAsyncSessionManager() as session:
            # Use async handlers for blog data
            posts = await get_all_blog_posts(session=session)
            categories = await get_blog_categories(session=session)
        
        return render_template(
            "marketing/blog.html",
            title="Blog",
            posts=posts,
            categories=categories
        )
    except Exception as e:
        logger.exception(f"Error loading blog posts: {e}")
        flash("Error loading blog posts.", "danger")
        return render_template(
            "marketing/blog.html",
            title="Blog",
            posts=[],
            categories=[]
        )


@marketing_bp.route("/blog/<slug>")
async def blog_post(slug):
    """Display individual blog post."""
    try:
        async with FlaskAsyncSessionManager() as session:
            post_data = await get_blog_post_by_slug(slug, session=session)
        
        if not post_data:
            flash("Blog post not found.", "warning")
            return redirect(url_for("marketing.blog"))

        return render_template("marketing/blog_post.html", title=post_data['title'], post=post_data)
    except Exception as e:
        logger.exception(f"Error loading blog post {slug}: {e}")
        flash("Error loading blog post.", "danger")
        return redirect(url_for("marketing.blog"))


# Lead Magnet Routes
@marketing_bp.route("/download/<magnet_name>")
async def download_lead_magnet(magnet_name):
    """Handle lead magnet downloads."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get email from form or query parameter
            email = request.args.get("email", "").strip().lower()

            # Validate email using helper
            if not _validate_email_address(email):
                flash("Please provide a valid email address to download.", "warning")
                return redirect(url_for("marketing.marketing_home"))

            # Get lead magnet data
            magnet = await get_lead_magnet_by_name(magnet_name, session=session)
            if not magnet:
                flash("Download not found.", "danger")
                return redirect(url_for("marketing.marketing_home"))

            # Prevent multiple downloads per day
            try:
                if await has_recent_download(magnet['id'], email, session):
                    flash("You've already downloaded this today. Check your email!", "info")
                    return redirect(url_for("marketing.marketing_home"))
            except SQLAlchemyError:
                # Already logged in helper; continue to allow download
                pass

            # Record download and increment count
            if not await record_download_and_increment(magnet['id'], email, session):
                flash("An error occurred while processing your download. Please try again later.", "danger")
                return redirect(url_for("marketing.marketing_home"))

            # Serve the file
            try:
                return _serve_lead_magnet_file(magnet, magnet_name)
            except OSError as os_err:
                logger.exception("Error serving lead magnet %s to %s: %s", magnet_name, email, os_err)
                flash("Download file not found. Please contact support.", "danger")
                return redirect(url_for("marketing.marketing_home"))

    except Exception:
        # Ensure any unexpected exception is recorded with full traceback to a dedicated file for easier diagnosis
        traceback_text = traceback.format_exc()
        logger.exception("Unhandled exception in download_lead_magnet for %s: %s", magnet_name, traceback_text)
        try:
            logs_dir = os.path.join(current_app.root_path, 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            with open(os.path.join(logs_dir, 'marketing_errors.log'), 'a', encoding='utf-8') as file_handle:
                file_handle.write("\n=== %s ===\n" % datetime.utcnow().isoformat())
                file_handle.write(traceback_text)
                file_handle.write('\n')
        except Exception:
            # best-effort: if writing log fails, continue
            logger.error('Failed to write marketing_errors.log')

        flash("An internal server error occurred. The team has been notified.", "danger")
        return redirect(url_for("marketing.marketing_home"))


@marketing_bp.route("/")
async def marketing_home():
    """Marketing homepage."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Use async handler for waitlist statistics
            stats = await get_waitlist_statistics(session=session)
            featured_posts = await get_all_blog_posts(limit=3, session=session)
        
        return render_template(
            "marketing/site.html",
            title="CultivAR - Professional Cannabis Grow Management",
            featured_posts=featured_posts,
            waitlist_count=stats.get("total", 0),
            today_signups=stats.get("today", 0)
        )
    except Exception as e:
        logger.exception(f"Error loading marketing homepage: {e}")
        flash("Error loading homepage content.", "danger")
        return render_template(
            "marketing/site.html",
            title="CultivAR - Professional Cannabis Grow Management",
            featured_posts=[],
            waitlist_count=0,
            today_signups=0
        )


# API Routes
@marketing_bp.route("/api/waitlist/stats")
async def waitlist_stats():
    """Get waitlist statistics for social proof."""
    try:
        async with FlaskAsyncSessionManager() as session:
            stats = await get_waitlist_statistics(session=session)
        return jsonify(stats)
    except Exception as e:
        logger.exception(f"Error getting waitlist stats: {e}")
        return jsonify({"total": 0, "today": 0, "this_week": 0}), 500


# Expose the marketing_home view for convenient top-level routing
__all__ = [
    'marketing_bp',
    'marketing_home'
]


@marketing_bp.route("/api/blog/search")
async def search_blog():
    """Search and filter blog posts.

    Behavior:
    - If only `category` is provided (no `q`), return recent posts in that category.
    - If `q` is provided (optionally with `category`), full-text search within published posts.
    - If neither is provided, return the most recent published posts.
    Response fields are shaped for app/web/static/js/blog.js expectations.
    """
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    try:
        async with FlaskAsyncSessionManager() as session:
            posts = await search_blog_posts(q, category, session=session)
        return jsonify({"posts": posts})
    except Exception as e:
        logger.exception(f"Error searching blog posts: {e}")
        return jsonify({"posts": []}), 500


# Error Handlers
@marketing_bp.errorhandler(404)
async def not_found(error):
    """Handle 404 errors."""
    return render_template("marketing/404.html", title="Page Not Found"), 404


@marketing_bp.errorhandler(500)
async def internal_error(error):
    """Handle 500 errors."""
    try:
        # In async context, we need to handle session cleanup differently
        logger.error(f"Marketing blueprint error: {error}")
    except Exception:
        pass
    return render_template("marketing/500.html", title="Server Error"), 500
