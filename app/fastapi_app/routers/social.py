"""
Social Media Router
Handles social media integration and sharing functionality (FastAPI version).
"""

from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import JSONResponse, RedirectResponse
from urllib.parse import quote
import logging

router = APIRouter(tags=["social"])
logger = logging.getLogger(__name__)


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


def generate_social_urls(base_url: str, title: str, description: str = None, hashtags: list = None):
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


@router.post("/share", name="social_share")
async def share_content(
    platform: str = Query(..., description="Social media platform"),
    url: str = Query(..., description="URL to share"),
    title: str = Query("Check out CultivAR!", description="Share title"),
    description: str = Query(None, description="Share description"),
    hashtags: str = Query(None, description="Comma-separated hashtags")
):
    """Handle social media sharing."""
    if not platform or not url:
        raise HTTPException(status_code=400, detail="Platform and URL required")

    if platform not in SOCIAL_PLATFORMS:
        raise HTTPException(status_code=400, detail="Invalid social media platform")

    # Parse hashtags
    hashtag_list = []
    if hashtags:
        hashtag_list = [tag.strip() for tag in hashtags.split(',') if tag.strip()]

    # Generate sharing URL
    social_urls = generate_social_urls(url, title, description, hashtag_list)
    share_url = social_urls.get(platform)

    if share_url:
        logger.info(f"Social share: {platform} - {url}")
        return RedirectResponse(url=share_url)

    raise HTTPException(status_code=500, detail="Error generating share URL")


@router.get("/share/blog/{slug}", name="social_share_blog")
async def share_blog_post(
    slug: str,
    request: Request,
    platform: str = Query(None, description="Specific platform to share to"),
    title: str = Query(None, description="Custom title"),
    description: str = Query(None, description="Custom description")
):
    """Generate social sharing URLs for a blog post."""
    try:
        # Get blog post data
        from app.models_async.marketing import BlogPost
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(BlogPost).where(
                    BlogPost.slug == slug,
                    BlogPost.is_published == True
                )
            )
            post = result.scalar_one_or_none()
            
            if not post:
                raise HTTPException(status_code=404, detail="Blog post not found")

        # Use post data or defaults
        post_title = title or f"Blog Post: {post.title}"
        post_description = description or post.excerpt or "Read this interesting blog post"
        
        # Build base URL
        base_url = str(request.url_for('site_blog_post', slug=slug))
        hashtags = ['cannabis', 'cultivation', 'growtips']
        
        # Generate social URLs
        social_urls = generate_social_urls(
            base_url=base_url,
            title=post_title,
            description=post_description,
            hashtags=hashtags
        )

        if platform:
            # Return specific platform URL
            if platform not in social_urls:
                raise HTTPException(status_code=400, detail="Invalid platform")
            return RedirectResponse(url=social_urls[platform])
        
        # Return all sharing URLs
        return JSONResponse({
            "post": {
                "title": post_title,
                "description": post_description,
                "url": base_url
            },
            "social_urls": social_urls,
            "platforms": SOCIAL_PLATFORMS
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating blog share URLs for {slug}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/follow", name="social_follow")
async def follow_links():
    """Get social media follow links."""
    social_links = {
        'twitter': 'https://twitter.com/cultivar_app',
        'facebook': 'https://facebook.com/cultivarapp',
        'instagram': 'https://instagram.com/cultivar_app',
        'linkedin': 'https://linkedin.com/company/cultivar-app',
        'youtube': 'https://youtube.com/cultivarapp',
        'discord': 'https://discord.gg/cultivar'
    }
    
    return JSONResponse({
        "title": "Follow Us",
        "social_links": social_links
    })


@router.get("/embed", name="social_embed")
async def embed_info():
    """Generate embed codes for social media."""
    return JSONResponse({
        "title": "Embed Codes",
        "message": "Social media embed functionality available"
    })


# API Routes
@router.get("/api/share-stats", name="social_share_stats")
async def share_stats():
    """Get social sharing statistics."""
    try:
        # This would typically come from a database table tracking shares
        # For now, return placeholder data
        return JSONResponse({
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
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/generate-share-url", name="social_generate_url")
async def generate_share_url(
    platform: str = Query(..., description="Social media platform"),
    url: str = Query(..., description="URL to share"),
    title: str = Query("Check out CultivAR!", description="Share title"),
    description: str = Query(None, description="Share description"),
    hashtags: str = Query(None, description="Comma-separated hashtags")
):
    """Generate a social media sharing URL."""
    try:
        if not platform or not url:
            raise HTTPException(status_code=400, detail="Platform and URL required")

        if platform not in SOCIAL_PLATFORMS:
            raise HTTPException(status_code=400, detail="Invalid platform")

        # Parse hashtags
        hashtag_list = []
        if hashtags:
            hashtag_list = [tag.strip() for tag in hashtags.split(',') if tag.strip()]

        social_urls = generate_social_urls(url, title, description, hashtag_list)
        share_url = social_urls.get(platform)

        if share_url:
            return JSONResponse({"share_url": share_url})

        raise HTTPException(status_code=500, detail="Failed to generate share URL")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Share URL generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Social Media Widgets
@router.get("/widgets/follow-buttons", name="social_follow_buttons")
async def follow_buttons(
    style: str = Query("horizontal", description="Button style: horizontal, vertical, compact"),
    platforms: str = Query("twitter,facebook,instagram", description="Comma-separated platform list")
):
    """Generate follow buttons for embedding."""
    platform_list = [p.strip() for p in platforms.split(',') if p.strip()]
    
    return JSONResponse({
        "platforms": platform_list,
        "style": style,
        "social_platforms": SOCIAL_PLATFORMS,
        "message": "Follow button widget configuration"
    })


@router.get("/widgets/share-buttons", name="social_share_buttons")
async def share_buttons(
    url: str = Query(None, description="URL to share"),
    title: str = Query("CultivAR - Professional Cannabis Grow Management", description="Share title"),
    style: str = Query("horizontal", description="Button style")
):
    """Generate share buttons for embedding."""
    if not url:
        # Use a default URL if none provided
        url = "https://cultivar.app"
    
    return JSONResponse({
        "url": url,
        "title": title,
        "style": style,
        "social_platforms": SOCIAL_PLATFORMS,
        "message": "Share button widget configuration"
    })


@router.get("/platforms", name="social_platforms")
async def get_platforms():
    """Get available social media platforms."""
    return JSONResponse({
        "platforms": SOCIAL_PLATFORMS,
        "count": len(SOCIAL_PLATFORMS)
    })


@router.get("/health", name="social_health")
async def health_check():
    """Health check endpoint for social router."""
    return JSONResponse({
        "status": "healthy",
        "service": "social",
        "platforms": list(SOCIAL_PLATFORMS.keys())
    })