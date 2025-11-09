"""
Utility functions for serializing data models for JSON responses.
"""

from datetime import datetime
from typing import Any, Dict, Optional


def serialize_blog_post(post) -> Dict[str, Any]:
    """
    Serialize a BlogPost model instance for JSON responses.

    Args:
        post: BlogPost SQLAlchemy model instance

    Returns:
        Dictionary with serialized blog post data
    """
    if not post:
        return {}

    return {
        "id": post.id,
        "title": post.title,
        "slug": post.slug,
        "excerpt": post.excerpt,
        "content": post.content,
        "author": post.author,
        "is_published": post.is_published,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "view_count": post.view_count or 0,
        "created_at": post.created_at.isoformat() if post.created_at else None,
        "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        "tags": getattr(post, "tags", []),
        "categories": getattr(post, "categories", []),
        "featured_image": getattr(post, "featured_image", None),
        "seo_title": getattr(post, "seo_title", None),
        "seo_description": getattr(post, "seo_description", None),
    }


def serialize_waitlist_entry(entry) -> Dict[str, Any]:
    """
    Serialize a Waitlist model instance for JSON responses.

    Args:
        entry: Waitlist SQLAlchemy model instance

    Returns:
        Dictionary with serialized waitlist data
    """
    if not entry:
        return {}

    return {
        "id": entry.id,
        "email": entry.email,
        "name": getattr(entry, "name", None),
        "experience": getattr(entry, "experience", None),
        "phone": getattr(entry, "phone", None),
        "referral_source": getattr(entry, "referral_source", None),
        "referral_code": getattr(entry, "referral_code", None),
        "priority_tier": getattr(entry, "priority_tier", None),
        "is_confirmed": getattr(entry, "is_confirmed", False),
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
        "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
    }


def serialize_lead_magnet(magnet) -> Dict[str, Any]:
    """
    Serialize a LeadMagnet model instance for JSON responses.

    Args:
        magnet: LeadMagnet SQLAlchemy model instance

    Returns:
        Dictionary with serialized lead magnet data
    """
    if not magnet:
        return {}

    return {
        "id": magnet.id,
        "name": magnet.name,
        "title": magnet.title,
        "description": getattr(magnet, "description", None),
        "file_path": getattr(magnet, "file_path", None),
        "is_active": getattr(magnet, "is_active", True),
        "download_count": getattr(magnet, "download_count", 0),
        "created_at": magnet.created_at.isoformat() if magnet.created_at else None,
        "updated_at": magnet.updated_at.isoformat() if magnet.updated_at else None,
    }
