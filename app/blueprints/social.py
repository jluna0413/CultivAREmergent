"""
Social media blueprint for the CultivAR application.
Handles social media integration and sharing functionality.
"""

from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, session
from urllib.parse import quote

from app.logger import logger
from app.models.base_models import db
from app.utils.rate_limiter import limiter

social_bp = Blueprint("social", __name__, url_prefix="/social", template_folder="../web/templates")


# Social Media Configuration
SOCIAL_PLATFORMS = {
    'twitter': {
        'name': 'Twitter',
        'url': 'https://twitter.com/intent/tweet',
        'color': '#1DA1F2',
        'icon': 'fab fa-twitter'
    },
    'facebook': {
        'name': 'Facebook',
        'url': 'https://www.facebook.com/sharer/sharer.php',
        'color': '#1877F2',
        'icon': 'fab fa-facebook-f'
    },
    'linkedin': {
        'name': 'LinkedIn',
        'url': 'https://www.linkedin.com/sharing/share-offsite',
        'color': '#0077B5',
        'icon': 'fab fa-linkedin-in'
    },
    'reddit': {
        'name': 'Reddit',
        'url': 'https://reddit.com/submit',
        'color': '#FF4500',
        'icon': 'fab fa-reddit-alien'
    },
    'whatsapp': {
        'name': 'WhatsApp',
        'url': 'https://wa.me',
        'color': '#25D366',
        'icon': 'fab fa-whatsapp'
    },
    'telegram': {
        'name': 'Telegram',
        'url': 'https://t.me/share/url',
        'color': '#0088CC',
        'icon': 'fab fa-telegram-plane'
    }
}


def generate_social_urls(base_url, title, description=None, hashtags=None):
    """Generate social media sharing URLs."""
    urls = {}

    for platform, config in SOCIAL_PLATFORMS.items():
        if platform == 'twitter':
            text = f"{title} {base_url}"
            if hashtags:
                text += f" {' '.join(hashtags)}"
            urls[platform] = f"{config['url']}?text={quote(text)}"

        elif platform == 'facebook':
            urls[platform] = f"{config['url']}?u={quote(base_url)}"

        elif platform == 'linkedin':
            urls[platform] = f"{config['url']}?url={quote(base_url)}"

        elif platform == 'reddit':
            urls[platform] = f"{config['url']}?url={quote(base_url)}&title={quote(title)}"

        elif platform == 'whatsapp':
            text = f"{title} - {base_url}"
            if description:
                text += f"\\n\\n{description}"
            urls[platform] = f"{config['url']}/?text={quote(text)}"

        elif platform == 'telegram':
            text = f"{title}\\n{base_url}"
            if description:
                text += f"\\n\\n{description}"
            urls[platform] = f"{config['url']}?url={quote(base_url)}&text={quote(text)}"

    return urls


@social_bp.route("/share", methods=["GET", "POST"])
def share():
    """Handle social media sharing."""
    if request.method == "POST":
        platform = request.form.get("platform")
        url = request.form.get("url")
        title = request.form.get("title", "Check out CultivAR!")
        description = request.form.get("description")

        if not platform or not url:
            flash("Missing required parameters.", "danger")
            return redirect(url_for("social.share"))

        if platform not in SOCIAL_PLATFORMS:
            flash("Invalid social media platform.", "danger")
            return redirect(url_for("social.share"))

        # Generate sharing URL
        social_urls = generate_social_urls(url, title, description)
        share_url = social_urls.get(platform)

        if share_url:
            logger.info(f"Social share: {platform} - {url}")
            return redirect(share_url)

        flash("Error generating share URL.", "danger")
        return redirect(url_for("social.share"))

    return render_template("social/share.html", title="Share", platforms=SOCIAL_PLATFORMS)


@social_bp.route("/share/blog/<slug>")
def share_blog_post(slug):
    """Generate social sharing URLs for a blog post."""
    from app.models.base_models import BlogPost

    post = BlogPost.query.filter_by(slug=slug, is_published=True).first()

    if not post:
        flash("Blog post not found.", "danger")
        return redirect(url_for("marketing.blog"))

    base_url = request.url_root.rstrip('/') + url_for("marketing.blog_post", slug=slug)
    social_urls = generate_social_urls(
        base_url=base_url,
        title=post.title,
        description=post.excerpt,
        hashtags=['cannabis', 'cultivation', 'growtips']
    )

    return render_template(
        "social/share_blog.html",
        title=f"Share: {post.title}",
        post=post,
        social_urls=social_urls,
        platforms=SOCIAL_PLATFORMS
    )


@social_bp.route("/follow")
def follow():
    """Display social media follow links."""
    social_links = {
        'twitter': 'https://twitter.com/cultivar_app',
        'facebook': 'https://facebook.com/cultivarapp',
        'instagram': 'https://instagram.com/cultivar_app',
        'linkedin': 'https://linkedin.com/company/cultivar-app',
        'youtube': 'https://youtube.com/cultivarapp',
        'discord': 'https://discord.gg/cultivar'
    }

    return render_template(
        "social/follow.html",
        title="Follow Us",
        social_links=social_links
    )


@social_bp.route("/embed")
def embed():
    """Generate embed codes for social media."""
    return render_template("social/embed.html", title="Embed Codes")


# API Routes
@social_bp.route("/api/share-stats")
def share_stats():
    """Get social sharing statistics."""
    try:
        # This would typically come from a database table tracking shares
        # For now, return placeholder data
        return jsonify({
            "total_shares": 0,
            "platform_breakdown": {
                "twitter": 0,
                "facebook": 0,
                "linkedin": 0,
                "reddit": 0,
                "whatsapp": 0,
                "telegram": 0
            },
            "top_posts": []
        })

    except Exception as e:
        logger.error(f"Social stats error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@social_bp.route("/api/generate-share-url")
def generate_share_url():
    """Generate a social media sharing URL."""
    try:
        platform = request.args.get("platform")
        url = request.args.get("url")
        title = request.args.get("title", "Check out CultivAR!")
        description = request.args.get("description")

        if not platform or not url:
            return jsonify({"error": "Platform and URL required"}), 400

        if platform not in SOCIAL_PLATFORMS:
            return jsonify({"error": "Invalid platform"}), 400

        social_urls = generate_social_urls(url, title, description)
        share_url = social_urls.get(platform)

        if share_url:
            return jsonify({"share_url": share_url})

        return jsonify({"error": "Failed to generate share URL"}), 500

    except Exception as e:
        logger.error(f"Share URL generation error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# Social Media Widgets
@social_bp.route("/widgets/follow-buttons")
def follow_buttons():
    """Generate follow buttons for embedding."""
    style = request.args.get("style", "horizontal")  # horizontal, vertical, compact
    platforms = request.args.get("platforms", "twitter,facebook,instagram").split(",")

    return render_template(
        "social/widgets/follow_buttons.html",
        platforms=platforms,
        style=style,
        social_platforms=SOCIAL_PLATFORMS
    )


@social_bp.route("/widgets/share-buttons")
def share_buttons():
    """Generate share buttons for embedding."""
    url = request.args.get("url", request.referrer or request.url_root)
    title = request.args.get("title", "CultivAR - Professional Cannabis Grow Management")
    style = request.args.get("style", "horizontal")

    return render_template(
        "social/widgets/share_buttons.html",
        url=url,
        title=title,
        style=style,
        social_platforms=SOCIAL_PLATFORMS
    )


# Error Handlers
@social_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("social/404.html", title="Page Not Found"), 404


@social_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Social blueprint error: {error}")
    return render_template("social/500.html", title="Server Error"), 500
