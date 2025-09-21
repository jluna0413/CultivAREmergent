"""
Marketing blueprint for the CultivAR application.
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

from app.logger import logger
from app.models.base_models import Waitlist, BlogPost, LeadMagnet, LeadMagnetDownload, db  # type: ignore
try:
    # Prefer the external validator when available for stricter checks
    from email_validator import validate_email, EmailNotValidError  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    validate_email = None  # type: ignore
    EmailNotValidError = None  # type: ignore

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


def _has_recent_download(magnet: LeadMagnet, email: str) -> bool:
    """Return True if the given email already downloaded this magnet today (UTC)."""
    try:
        utc_now = datetime.utcnow()
        start_of_utc_day = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
        recent = LeadMagnetDownload.query.filter_by(
            lead_magnet_id=magnet.id,
            email=email
        ).filter(LeadMagnetDownload.download_date >= start_of_utc_day).first()
        return recent is not None
    except SQLAlchemyError:
        logger.exception("DB error when checking recent download for %s", email)
        return False


def _record_download_and_increment(magnet: LeadMagnet, email: str) -> bool:
    """Create a LeadMagnetDownload record and increment magnet.download_count.

    Returns True on success, False on DB error.
    """
    try:
        download = LeadMagnetDownload(
            lead_magnet_id=magnet.id,
            email=email,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string[:255]
        )
        magnet.download_count = (magnet.download_count or 0) + 1
        db.session.add(download)
        db.session.add(magnet)
        db.session.commit()
        logger.info("Lead magnet downloaded: %s by %s", magnet.name, email)
        return True
    except SQLAlchemyError:
        db.session.rollback()
        logger.exception("Failed to record download for %s", email)
        return False


def _serve_lead_magnet_file(magnet: LeadMagnet, magnet_name: str):
    """Return a Flask response for the magnet file or raise OSError if not found."""
    safe_dir = current_app.config.get('LEAD_MAGNET_DIR', os.path.join(current_app.root_path, 'static', 'lead_magnets'))
    safe_dir_abs = os.path.abspath(safe_dir)
    filename = os.path.basename(magnet.file_path)
    file_path = os.path.join(safe_dir_abs, filename)

    if not os.path.exists(file_path):
        raise OSError(f"Lead magnet file not found: {file_path}")

    return send_from_directory(safe_dir_abs, filename, as_attachment=True, download_name=f"{secure_filename(magnet_name)}.pdf")



# Waitlist Routes
@marketing_bp.route("/waitlist", methods=["GET", "POST"])
def waitlist():
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

        # Check if email already exists
        existing = Waitlist.query.filter_by(email=email).first()
        if existing:
            flash("This email is already on the waitlist!", "info")
            return redirect(url_for("marketing.waitlist"))

        # Generate referral code
        new_referral_code = secrets.token_urlsafe(8)

        # Handle referral
        referred_by = None
        if referral_code:
            referrer = Waitlist.query.filter_by(referral_code=referral_code).first()
            if referrer:
                referred_by = referrer.id

        # Create waitlist entry
        waitlist_entry = Waitlist(
            email=email,
            priority_tier=priority_tier,
            referral_code=new_referral_code,
            referred_by=referred_by,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string[:255]
        )

        db.session.add(waitlist_entry)
        db.session.commit()

        logger.info("New waitlist signup: %s (tier: %s)", email, priority_tier)

        flash("Welcome to the waitlist! Check your email for next steps.", "success")
        return redirect(url_for("marketing.waitlist_success", code=new_referral_code))

    return render_template("marketing/waitlist.html", title="Join the Waitlist")


@marketing_bp.route("/waitlist/success/<code>")
def waitlist_success(code):
    """Show waitlist success page with referral code."""
    waitlist_entry = Waitlist.query.filter_by(referral_code=code).first_or_404()
    return render_template(
        "marketing/waitlist_success.html",
        title="Welcome to the Waitlist",
        referral_code=waitlist_entry.referral_code,
        email=waitlist_entry.email
    )


# Blog Routes
@marketing_bp.route("/blog")
def blog():
    """Display blog posts."""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)

    # Query published posts
    query = BlogPost.query.filter_by(is_published=True)

    if category:
        query = query.filter_by(category=category)

    posts = query.order_by(BlogPost.publish_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    # Get all categories for filter
    categories = db.session.query(BlogPost.category).filter(
        BlogPost.category.isnot(None),
        BlogPost.is_published == True
    ).distinct().all()

    return render_template(
        "marketing/blog.html",
        title="Blog",
        posts=posts,
        categories=[cat[0] for cat in categories if cat[0]]
    )


@marketing_bp.route("/blog/<slug>")
def blog_post(slug):
    """Display individual blog post."""
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Increment view count
    post.view_count += 1
    db.session.commit()

    return render_template("marketing/blog_post.html", title=post.title, post=post)


# Lead Magnet Routes
@marketing_bp.route("/download/<magnet_name>")
def download_lead_magnet(magnet_name):
    """Handle lead magnet downloads."""
    try:
        magnet = LeadMagnet.query.filter_by(name=magnet_name, is_active=True).first()

        if not magnet:
            flash("Download not found.", "danger")
            return redirect(url_for("marketing.marketing_home"))

        # Get email from form or query parameter
        email = request.args.get("email", "").strip().lower()

        # Validate email using helper
        if not _validate_email_address(email):
            flash("Please provide a valid email address to download.", "warning")
            return redirect(url_for("marketing.marketing_home"))

        # Prevent multiple downloads per day
        try:
            if _has_recent_download(magnet, email):
                flash("You've already downloaded this today. Check your email!", "info")
                return redirect(url_for("marketing.marketing_home"))
        except SQLAlchemyError:
            # Already logged in helper; continue to allow download
            pass

        # Record download and increment count
        if not _record_download_and_increment(magnet, email):
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
def marketing_home():
    """Marketing homepage."""
    # Get featured blog posts
    featured_posts = BlogPost.query.filter_by(is_published=True).order_by(
        BlogPost.publish_date.desc()
    ).limit(3).all()

    # Get waitlist stats for social proof
    waitlist_count = Waitlist.query.count()
    today_signups = Waitlist.query.filter(
        Waitlist.signup_date >= datetime.utcnow().replace(hour=0, minute=0, second=0)
    ).count()

    return render_template(
        "marketing/site.html",
        title="CultivAR - Professional Cannabis Grow Management",
        featured_posts=featured_posts,
        waitlist_count=waitlist_count,
        today_signups=today_signups
    )


# API Routes
@marketing_bp.route("/api/waitlist/stats")
def waitlist_stats():
    """Get waitlist statistics for social proof."""
    total = Waitlist.query.count()
    today = Waitlist.query.filter(
        Waitlist.signup_date >= datetime.utcnow().replace(hour=0, minute=0, second=0)
    ).count()
    this_week = Waitlist.query.filter(
        Waitlist.signup_date >= datetime.utcnow() - timedelta(days=7)
    ).count()

    return jsonify({
        "total": total,
        "today": today,
        "this_week": this_week
    })


# Expose the marketing_home view for convenient top-level routing
__all__ = [
    'marketing_bp',
    'marketing_home'
]


@marketing_bp.route("/api/blog/search")
def search_blog():
    """Search and filter blog posts.

    Behavior:
    - If only `category` is provided (no `q`), return recent posts in that category.
    - If `q` is provided (optionally with `category`), full-text search within published posts.
    - If neither is provided, return the most recent published posts.
    Response fields are shaped for app/web/static/js/blog.js expectations.
    """
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    # Base query: published posts only
    query = BlogPost.query.filter(BlogPost.is_published == True)

    # Optional category filter
    if category:
        query = query.filter(BlogPost.category == category)

    # Optional text search
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                BlogPost.title.ilike(like),  # type: ignore
                BlogPost.content.ilike(like),  # type: ignore
                BlogPost.excerpt.ilike(like),  # type: ignore
                BlogPost.tags.ilike(like)  # type: ignore
            )
        )

    posts = query.order_by(BlogPost.publish_date.desc()).limit(10).all()

    def fmt_date(dt):
        try:
            return dt.strftime("%b %d, %Y") if dt else ""
        except Exception:
            return ""

    return jsonify({
        "posts": [{
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "excerpt": post.excerpt or (post.content[:150] + '...') if post.content else "",
            "author": post.author or "CultivAR Team",
            "category": post.category or "General",
            # Fields expected by blog.js renderer
            "url": url_for('marketing.blog_post', slug=post.slug),
            "date": fmt_date(post.publish_date),
            "isoDate": post.publish_date.isoformat() if getattr(post, 'publish_date', None) else "",
            "imageUrl": post.featured_image or "",
            "imageAlt": post.title
        } for post in posts]
    })


# Error Handlers
@marketing_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("marketing/404.html", title="Page Not Found"), 404


@marketing_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    logger.error(f"Marketing blueprint error: {error}")
    return render_template("marketing/500.html", title="Server Error"), 500
