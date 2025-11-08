"""
Marketing handlers for the CultivAR application - ASYNC VERSION.
Handles waitlist, blog, and lead magnet functionality with async database operations.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import select, and_, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import (
    Waitlist, BlogPost, LeadMagnet, LeadMagnetDownload, NewsletterSubscriber
)


# Waitlist Handlers

async def create_waitlist_entry(email: str, priority_tier: str = 'general', 
                               referral_code: Optional[str] = None, referred_by: Optional[int] = None, 
                               session: AsyncSession = None, 
                               ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new waitlist entry - ASYNC VERSION.
    
    Args:
        email: Email address for waitlist signup
        priority_tier: Priority tier (early_bird, beta, general)
        referral_code: Unique referral code
        referred_by: ID of referring user
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        # Check if email already exists
        existing = await session.execute(
            select(Waitlist).where(Waitlist.email == email)
        )
        if existing.scalars().first():
            return {"success": False, "error": "Email already registered"}
        
        # Create new waitlist entry
        new_entry = Waitlist(
            email=email,
            priority_tier=priority_tier,
            referral_code=referral_code,
            referred_by=referred_by,
            ip_address=ip_address,
            user_agent=user_agent[:255] if user_agent else None
        )
        
        session.add(new_entry)
        await session.commit()
        await session.refresh(new_entry)
        
        logger.info("New waitlist signup: %s (tier: %s)", email, priority_tier)
        
        return {
            "success": True,
            "waitlist_id": new_entry.id,
            "referral_code": new_entry.referral_code,
            "message": "Welcome to the waitlist!"
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating waitlist entry: {e}")
        return {"success": False, "error": str(e)}


async def get_waitlist_count(session: AsyncSession = None) -> int:
    """
    Get total waitlist count - ASYNC VERSION.
    
    Args:
        session: AsyncSession for database operations
    
    Returns:
        int: Total number of waitlist entries
    """
    try:
        result = await session.execute(select(Waitlist))
        waitlist_entries = result.scalars().all()
        return len(waitlist_entries)
    except Exception as e:
        logger.error(f"Error getting waitlist count: {e}")
        return 0


async def get_waitlist_signups_today(session: AsyncSession = None) -> int:
    """
    Get today's waitlist signups - ASYNC VERSION.
    
    Args:
        session: AsyncSession for database operations
    
    Returns:
        int: Number of signups today
    """
    try:
        today = datetime.utcnow().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        
        result = await session.execute(
            select(Waitlist).where(Waitlist.signup_date >= start_of_day)
        )
        today_signups = result.scalars().all()
        return len(today_signups)
    except Exception as e:
        logger.error(f"Error getting today's waitlist signups: {e}")
        return 0


async def get_waitlist_statistics(session: AsyncSession = None) -> Dict[str, int]:
    """
    Get comprehensive waitlist statistics - ASYNC VERSION.
    
    Args:
        session: AsyncSession for database operations
    
    Returns:
        Dict[str, int]: Waitlist statistics
    """
    try:
        total = await get_waitlist_count(session)
        today = await get_waitlist_signups_today(session)
        
        # Get this week's signups
        week_ago = datetime.utcnow() - timedelta(days=7)
        result = await session.execute(
            select(Waitlist).where(Waitlist.signup_date >= week_ago)
        )
        this_week = len(result.scalars().all())
        
        return {
            "total": total,
            "today": today,
            "this_week": this_week
        }
    except Exception as e:
        logger.error(f"Error getting waitlist statistics: {e}")
        return {"total": 0, "today": 0, "this_week": 0}


# Blog Handlers

async def get_all_blog_posts(limit: int = None, category: str = None, 
                           session: AsyncSession = None) -> List[Dict[str, Any]]:
    """
    Get all published blog posts - ASYNC VERSION.
    
    Args:
        limit: Maximum number of posts to return
        category: Filter by category
        session: AsyncSession for database operations
    
    Returns:
        List[Dict[str, Any]]: List of blog post data dictionaries
    """
    try:
        query = select(BlogPost).where(BlogPost.is_published == True)
        
        if category:
            query = query.where(BlogPost.category == category)
        
        query = query.order_by(desc(BlogPost.publish_date))
        
        if limit:
            query = query.limit(limit)
        
        result = await session.execute(query)
        posts = result.scalars().all()
        
        post_list = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "excerpt": post.excerpt or "",
                "content": post.content[:200] + "..." if len(post.content) > 200 else post.content,
                "category": post.category or "",
                "author": post.author or "",
                "publish_date": post.publish_date.strftime("%Y-%m-%d") if post.publish_date else "",
                "featured_image": post.featured_image,
                "view_count": post.view_count or 0,
                "reading_time": post.reading_time
            }
            post_list.append(post_data)
        
        return post_list
    except Exception as e:
        logger.error(f"Error getting blog posts: {e}")
        return []


async def get_blog_post_by_slug(slug: str, session: AsyncSession = None) -> Optional[Dict[str, Any]]:
    """
    Get a single blog post by slug - ASYNC VERSION.
    
    Args:
        slug: Blog post slug
        session: AsyncSession for database operations
    
    Returns:
        Optional[Dict[str, Any]]: Blog post data dictionary or None
    """
    try:
        result = await session.execute(
            select(BlogPost).where(and_(BlogPost.slug == slug, BlogPost.is_published == True))
        )
        post = result.scalars().first()
        
        if not post:
            return None
        
        # Increment view count
        post.view_count = (post.view_count or 0) + 1
        await session.commit()
        
        post_data = {
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "content": post.content,
            "excerpt": post.excerpt or "",
            "category": post.category or "",
            "author": post.author or "",
            "publish_date": post.publish_date.strftime("%Y-%m-%d") if post.publish_date else "",
            "featured_image": post.featured_image,
            "meta_description": post.meta_description or "",
            "tags": post.tags_list,
            "view_count": post.view_count,
            "reading_time": post.reading_time
        }
        
        return post_data
    except Exception as e:
        logger.error(f"Error getting blog post by slug: {e}")
        return None


async def search_blog_posts(query: str, category: str = None, 
                          session: AsyncSession = None) -> List[Dict[str, Any]]:
    """
    Search and filter blog posts - ASYNC VERSION.
    
    Args:
        query: Search query
        category: Filter by category
        session: AsyncSession for database operations
    
    Returns:
        List[Dict[str, Any]]: List of matching blog post data dictionaries
    """
    try:
        search_query = select(BlogPost).where(BlogPost.is_published == True)
        
        if query:
            search_query = search_query.where(
                or_(
                    BlogPost.title.contains(query),
                    BlogPost.content.contains(query),
                    BlogPost.excerpt.contains(query)
                )
            )
        
        if category:
            search_query = search_query.where(BlogPost.category == category)
        
        search_query = search_query.order_by(desc(BlogPost.publish_date))
        
        result = await session.execute(search_query)
        posts = result.scalars().all()
        
        post_list = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "excerpt": post.excerpt or "",
                "category": post.category or "",
                "author": post.author or "",
                "publish_date": post.publish_date.strftime("%Y-%m-%d") if post.publish_date else "",
                "featured_image": post.featured_image,
                "view_count": post.view_count or 0,
                "reading_time": post.reading_time
            }
            post_list.append(post_data)
        
        return post_list
    except Exception as e:
        logger.error(f"Error searching blog posts: {e}")
        return []


async def get_blog_categories(session: AsyncSession = None) -> List[str]:
    """
    Get all unique blog categories - ASYNC VERSION.
    
    Args:
        session: AsyncSession for database operations
    
    Returns:
        List[str]: List of unique categories
    """
    try:
        result = await session.execute(
            select(BlogPost.category).where(
                and_(BlogPost.category.isnot(None), BlogPost.is_published == True)
            ).distinct()
        )
        categories = result.scalars().all()
        return [cat for cat in categories if cat]
    except Exception as e:
        logger.error(f"Error getting blog categories: {e}")
        return []


# Lead Magnet Handlers

async def get_lead_magnet_by_name(name: str, session: AsyncSession = None) -> Optional[Dict[str, Any]]:
    """
    Get a lead magnet by name - ASYNC VERSION.
    
    Args:
        name: Lead magnet name
        session: AsyncSession for database operations
    
    Returns:
        Optional[Dict[str, Any]]: Lead magnet data dictionary or None
    """
    try:
        result = await session.execute(
            select(LeadMagnet).where(and_(LeadMagnet.name == name, LeadMagnet.is_active == True))
        )
        magnet = result.scalars().first()
        
        if not magnet:
            return None
        
        return {
            "id": magnet.id,
            "name": magnet.name,
            "description": magnet.description or "",
            "file_path": magnet.file_path,
            "download_count": magnet.download_count or 0,
            "is_active": magnet.is_active
        }
    except Exception as e:
        logger.error(f"Error getting lead magnet by name: {e}")
        return None


async def has_recent_download(magnet_id: int, email: str, session: AsyncSession = None) -> bool:
    """
    Check if email already downloaded this magnet today - ASYNC VERSION.
    
    Args:
        magnet_id: Lead magnet ID
        email: User email
        session: AsyncSession for database operations
    
    Returns:
        bool: True if recent download exists
    """
    try:
        utc_now = datetime.utcnow()
        start_of_utc_day = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        result = await session.execute(
            select(LeadMagnetDownload).where(
                and_(
                    LeadMagnetDownload.lead_magnet_id == magnet_id,
                    LeadMagnetDownload.email == email,
                    LeadMagnetDownload.download_date >= start_of_utc_day
                )
            )
        )
        recent = result.scalars().first()
        return recent is not None
    except Exception as e:
        logger.error(f"Error checking recent download for %s: {e}", email)
        return False


async def record_download_and_increment(magnet_id: int, email: str, 
                                      session: AsyncSession = None, 
                                      ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> bool:
    """
    Record a lead magnet download and increment count - ASYNC VERSION.
    
    Args:
        magnet_id: Lead magnet ID
        email: User email
        session: AsyncSession for database operations
    
    Returns:
        bool: True on success
    """
    try:
        # Get the magnet
        result = await session.execute(select(LeadMagnet).where(LeadMagnet.id == magnet_id))
        magnet = result.scalars().first()
        
        if not magnet:
            return False
        
        # Create download record
        download = LeadMagnetDownload(
            lead_magnet_id=magnet_id,
            email=email,
            ip_address=ip_address,
            user_agent=user_agent[:255] if user_agent else None
        )
        
        # Increment magnet download count
        magnet.download_count = (magnet.download_count or 0) + 1
        
        session.add(download)
        session.add(magnet)
        await session.commit()
        
        logger.info("Lead magnet downloaded: %s by %s", magnet.name, email)
        return True
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to record download for %s: {e}", email)
        return False


# Newsletter Handlers

async def subscribe_newsletter(email: str, phone: str = None, 
                             subscription_type: str = 'both', 
                             source: str = 'website',
                             session: AsyncSession = None, ip_address: str = None) -> Dict[str, Any]:
    """
    Subscribe to newsletter - ASYNC VERSION.
    
    Args:
        email: Email address
        phone: Phone number (optional)
        subscription_type: email, phone, or both
        source: Subscription source
        session: AsyncSession for database operations
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        # Check if already subscribed
        existing = await session.execute(
            select(NewsletterSubscriber).where(
                or_(
                    NewsletterSubscriber.email == email,
                    NewsletterSubscriber.phone == phone
                )
            )
        )
        
        if existing.scalars().first():
            return {"success": False, "error": "Already subscribed"}
        
        # Create new subscription
        subscriber = NewsletterSubscriber(
            email=email,
            phone=phone,
            subscription_type=subscription_type,
            source=source,
            ip_address=ip_address
        )
        
        session.add(subscriber)
        await session.commit()
        await session.refresh(subscriber)
        
        logger.info("Newsletter subscription: %s (%s)", email, subscription_type)
        
        return {
            "success": True,
            "subscriber_id": subscriber.id,
            "message": "Successfully subscribed!"
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating newsletter subscription: {e}")
        return {"success": False, "error": str(e)}