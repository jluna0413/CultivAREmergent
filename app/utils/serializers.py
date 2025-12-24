"""
Serializers for converting SQLAlchemy models to dictionaries.
"""

from app.models_async.marketing import BlogPost

def serialize_blog_post(post: BlogPost) -> dict:
    """
    Serializes a BlogPost object to a dictionary.
    """
    def fmt_date(dt):
        try:
            return dt.strftime("%b %d, %Y") if dt else ""
        except Exception:
            return ""

    return {
        "id": post.id,
        "title": post.title,
        "slug": post.slug,
        "excerpt": post.excerpt or (post.content[:150] + '...') if post.content else "",
        "author": post.author_rel.username if post.author_rel else "CultivAR Team",
        "category": post.categories[0] if post.categories else "General",
        "url": f"/blog/{post.slug}",
        "date": fmt_date(post.published_at),
        "isoDate": post.published_at.isoformat() if getattr(post, 'published_at', None) else "",
        "imageUrl": post.featured_image or "",
        "imageAlt": post.title
    }
