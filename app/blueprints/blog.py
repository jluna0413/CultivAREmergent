"""
Blog blueprint for the CultivAR application - ASYNC VERSION.
Handles blog functionality with async database operations.
"""

import traceback
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from app.logger import logger
from app.utils.async_flask_helpers import FlaskAsyncSessionManager

# Import async handlers
from app.handlers.marketing_handlers_async import (
    get_all_blog_posts,
    get_blog_post_by_slug,
    search_blog_posts,
    get_blog_categories
)

blog_bp = Blueprint("blog", __name__, url_prefix="/blog", template_folder="../web/templates")


@blog_bp.route("")
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


@blog_bp.route("/<slug>")
async def blog_post(slug):
    """Display individual blog post."""
    try:
        async with FlaskAsyncSessionManager() as session:
            post_data = await get_blog_post_by_slug(slug, session=session)
        
        if not post_data:
            flash("Blog post not found.", "warning")
            return redirect(url_for("blog.blog"))

        return render_template("marketing/blog_post.html", title=post_data['title'], post=post_data)
    except Exception as e:
        logger.exception(f"Error loading blog post {slug}: {e}")
        flash("Error loading blog post.", "danger")
        return redirect(url_for("blog.blog"))


@blog_bp.route("/search")
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
@blog_bp.errorhandler(404)
async def not_found(error):
    """Handle 404 errors."""
    return render_template("marketing/404.html", title="Page Not Found"), 404


@blog_bp.errorhandler(500)
async def internal_error(error):
    """Handle 500 errors."""
    try:
        # In async context, we need to handle session cleanup differently
        logger.error(f"Blog blueprint error: {error}")
    except Exception:
        pass
    return render_template("marketing/500.html", title="Server Error"), 500


# Expose the blog view for convenient routing
__all__ = [
    'blog_bp',
    'blog'
]