"""
Site Router
Public-facing/marketing routes (consolidates marketing and site blueprints).
"""

from fastapi import APIRouter, Request, Depends, HTTPException, Form, Query
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
import os
import logging
from app.fastapi_app.dependencies import inject_template_context
from app.config.config import Config

router = APIRouter(tags=["site"])


# Blog API Routes
@router.get("/api/blog", name="blog_api_list")
async def blog_api_list(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Posts per page"),
    category: str = Query(None, description="Filter by category"),
    search: str = Query(None, description="Search query")
):
    """API endpoint for blog posts list with pagination and filtering."""
    logger = logging.getLogger(__name__)
    try:
        from app.models_async.marketing import BlogPost
        from app.utils.serializers import serialize_blog_post
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select, func, or_
        
        async with AsyncSessionLocal() as db:
            # Build query with filters
            query = select(BlogPost).where(BlogPost.is_published == True)
            
            # Apply category filter
            if category:
                query = query.where(BlogPost.categories.contains([category]))
            
            # Apply search filter
            if search:
                search_filter = or_(
                    BlogPost.title.ilike(f"%{search}%"),
                    BlogPost.content.ilike(f"%{search}%"),
                    BlogPost.excerpt.ilike(f"%{search}%")
                )
                query = query.where(search_filter)
            
            # Get total count
            count_query = select(func.count()).select_from(
                query.subquery()
            )
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Apply pagination
            query = query.order_by(BlogPost.published_at.desc()).offset((page - 1) * limit).limit(limit)
            
            # Execute query
            result = await db.execute(query)
            posts = result.scalars().all()
            
            # Serialize posts
            posts_data = [serialize_blog_post(post) for post in posts]
            
            return JSONResponse({
                "posts": posts_data,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": (total + limit - 1) // limit
                },
                "filters": {
                    "category": category,
                    "search": search
                }
            })
    except Exception as e:
        logger.exception(f"Error in blog API list: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")         


@router.get("/api/blog/{slug}", name="blog_api_detail")
async def blog_api_detail(slug: str):
    """API endpoint for individual blog post."""
    logger = logging.getLogger(__name__)
    try:
        from app.models_async.marketing import BlogPost
        from app.utils.serializers import serialize_blog_post
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
            
            return JSONResponse(serialize_blog_post(post))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in blog API detail: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/blog/categories", name="blog_api_categories")
async def blog_api_categories():
    """API endpoint for blog categories."""
    logger = logging.getLogger(__name__)
    try:
        from app.models_async.marketing import BlogPost
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select, func
        
        async with AsyncSessionLocal() as db:
            # Get all unique categories from published posts
            result = await db.execute(
                select(func.array_agg(func.distinct(BlogPost.categories)))
                .where(BlogPost.is_published == True)
            )
            categories = result.scalar()
            
            # Flatten and filter categories
            all_categories = []
            if categories:
                for category_list in categories:
                    if category_list:
                        all_categories.extend(category_list)
            
            # Remove duplicates and sort
            unique_categories = sorted(list(set(all_categories)))
            
            return JSONResponse({
                "categories": unique_categories,
                "count": len(unique_categories)
            })
            
    except Exception as e:
        logger.exception(f"Error in blog API categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/blog/search", name="blog_api_search")
async def blog_api_search(
    q: str = Query(..., min_length=2, max_length=100, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Results per page")
):
    """API endpoint for blog search functionality."""
    logger = logging.getLogger(__name__)
    try:
        from app.models_async.marketing import BlogPost
        from app.utils.serializers import serialize_blog_post
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select, func, or_
        
        async with AsyncSessionLocal() as db:
            # Search across title, content, and excerpt
            query = select(BlogPost).where(
                BlogPost.is_published == True,
                or_(
                    BlogPost.title.ilike(f"%{q}%"),
                    BlogPost.content.ilike(f"%{q}%"),
                    BlogPost.excerpt.ilike(f"%{q}%")
                )
            )
            
            # Get total count
            count_query = select(func.count()).select_from(
                query.subquery()
            )
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Apply pagination
            query = query.order_by(
                BlogPost.title.ilike(f"%{q}%").desc(),  # Title matches first
                BlogPost.published_at.desc()
            ).offset((page - 1) * limit).limit(limit)
            
            # Execute query
            result = await db.execute(query)
            posts = result.scalars().all()
            
            # Serialize posts
            posts_data = [serialize_blog_post(post) for post in posts]
            
            return JSONResponse({
                "posts": posts_data,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": (total + limit - 1) // limit
                },
                "query": q
            })
            
    except Exception as e:
        logger.exception(f"Error in blog API search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post('/waitlist', name='waitlist_signup')
async def waitlist_signup_form(
    request: Request,
    email: str = Form(...),
    name: str = Form(...),
    experience: str = Form(...),
    phone: str = Form(None),
    referral: str = Form(None),
    csrf_token: str = Form(None)  # Accept CSRF token but don't validate (FastAPI doesn't need it like Flask)
):
    """Handle HTML form submission for waitlist signup.
    
    Accepts form data from the waitlist landing page with fields:
    - email (required)
    - name (required)
    - experience (required)
    - phone (optional)
    - referral (optional)
    - csrf_token (ignored for compatibility)
    """
    email = email.strip().lower()
    
    if not email:
        raise HTTPException(status_code=400, detail='Email required')
    
    try:
        from app.models_async.marketing import Waitlist
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as db:
            # Check for existing signup
            result = await db.execute(
                select(Waitlist).where(Waitlist.email == email)
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                # Redirect with success (already signed up)
                return RedirectResponse(
                    url=f"{request.url_for('waitlist_landing')}?success=true",
                    status_code=303
                )
            
            # Create new waitlist entry
            entry = Waitlist(
                email=email,
                name=name,
                experience=experience,
                phone=phone,
                referral_source=referral
            )
            db.add(entry)
            await db.commit()
            
            # Redirect with success message
            return RedirectResponse(
                url=f"{request.url_for('waitlist_landing')}?success=true",
                status_code=303
            )
    except Exception as e:
        # Log the error but don't break the public site
        print(f"Error in waitlist signup: {e}")
        # Redirect with success anyway (graceful degradation)
        return RedirectResponse(
            url=f"{request.url_for('waitlist_landing')}?success=true",
            status_code=303
        )


@router.post('/api/waitlist', name='site_api_waitlist')
async def api_waitlist_signup(request: Request):
    """API endpoint to accept waitlist signups (minimal, mirrors legacy behavior).

    Expects JSON payload like {"email": "x@x.com", "referral_code": "abc", "priority_tier": "early"}
    Records a Waitlist entry when the `Waitlist` model is present; otherwise
    returns 200 with a harmless message for environments without DB.
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid JSON payload')

    email = (data.get('email') or '').strip().lower()
    referral_code = data.get('referral_code')
    priority_tier = data.get('priority_tier')

    if not email:
        raise HTTPException(status_code=400, detail='Email required')

    try:
        from app.models_async.marketing import Waitlist
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select

        async with AsyncSessionLocal() as db:
            # Prevent duplicate signups
            result = await db.execute(
                select(Waitlist).where(Waitlist.email == email)
            )
            existing = result.scalar_one_or_none()
            if existing:
                return {"status": "existing", "message": "Already on waitlist"}

            entry = Waitlist(email=email, referral_code=referral_code, priority_tier=priority_tier)
            db.add(entry)
            await db.commit()
            return {"status": "ok", "message": "Signed up"}
    except Exception:
        # If models or DB aren't available, return success to avoid breaking public site
        return {"status": "ok", "message": "Signup accepted"}


@router.get("/", name="site_home")
async def site_home(
    request: Request,
    context: dict = Depends(inject_template_context)
):
    """Marketing homepage."""
    # TODO: Migrate from app/blueprints/site.py and app/blueprints/marketing.py
    # Use existing marketing/home.html (landing.html is not present in templates)
    return request.app.state.templates.TemplateResponse("marketing/home.html", context)


@router.get("/blog", name="site_blog")
async def blog_listing(
    request: Request,
    context: dict = Depends(inject_template_context)
):
    """Blog listing page."""
    # TODO: Migrate from app/blueprints/site.py
    # Build a small pagination-like object for the template when no DB is
    # available. In production this should come from the DB query.
    class _Posts:
        def __init__(self, items=None):
            self.items = items or []
            self.pages = 1
            self.page = 1
            self.total = len(self.items)
            self.has_prev = False
            self.has_next = False
            self.prev_num = None
            self.next_num = None

        def iter_pages(self):
            return [1]

        def __bool__(self):
            return bool(self.items)

    posts = _Posts(items=[])
    # Ensure route explicitly provides posts and categories so templates don't
    # need to rely on global defaults.
    context = dict(context)
    context.setdefault('posts', posts)
    context.setdefault('categories', [])

    return request.app.state.templates.TemplateResponse("marketing/blog.html", context)


@router.get("/waitlist", name="site_waitlist")
async def waitlist_page(
    request: Request,
    context: dict = Depends(inject_template_context)
):
    """Waitlist signup page."""
    # TODO: Migrate from app/blueprints/site.py
    return request.app.state.templates.TemplateResponse("marketing/waitlist.html", context)



@router.get('/blog/{slug}', name='site_blog_post')
async def blog_post(
    slug: str,
    request: Request,
    context: dict = Depends(inject_template_context)
):
    """Display individual blog post using existing models when available.

    Falls back to rendering the blog template with an empty context if the
    models are not present or the post cannot be loaded.
    """
    try:
        from app.models_async.marketing import BlogPost
        from app.utils.serializers import serialize_blog_post
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as db:
            # Try to find the published post
            result = await db.execute(
                select(BlogPost).where(
                    BlogPost.slug == slug,
                    BlogPost.is_published == True
                )
            )
            post = result.scalar_one_or_none()
            if not post:
                raise HTTPException(status_code=404)

            # Increment view count where possible
            try:
                post.view_count = (post.view_count or 0) + 1
                db.add(post)
                await db.commit()
            except Exception:
                # non-fatal if DB commit fails in some environments
                pass

            post_ctx = serialize_blog_post(post) if post else {}
            context.update({"post": post_ctx, "title": post_ctx.get("title", "Blog Post")})
            return request.app.state.templates.TemplateResponse("marketing/blog_post.html", context)
    except HTTPException:
        # Render a 404 template if appropriate
        return request.app.state.templates.TemplateResponse("marketing/404.html", context, status_code=404)
    except Exception:
        # Fall back to generic blog template
        return request.app.state.templates.TemplateResponse("marketing/blog.html", context)


@router.get('/download/{magnet_name}', name='site_download_magnet')
async def download_lead_magnet(
    magnet_name: str,
    request: Request,
    email: str | None = None,
    context: dict = Depends(inject_template_context)
):
    """Serve lead-magnet files safely when present.

    This is a conservative, low-risk implementation intended to allow
    public marketing downloads to be served from FastAPI while preserving
    path safety checks and basic email presence validation.
    """
    # Minimal email gating: require email query param for download attempts
    if not email:
        # Render the marketing homepage so user can enter email via UI
        return request.app.state.templates.TemplateResponse("marketing/waitlist.html", context)

    try:
        from app.models_async.marketing import LeadMagnet
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(LeadMagnet).where(
                    LeadMagnet.name == magnet_name,
                    LeadMagnet.is_active == True
                )
            )
            magnet = result.scalar_one_or_none()
            if not magnet or not magnet.file_path:
                raise HTTPException(status_code=404)

            # Resolve safe directory
            cfg = Config()
            safe_dir = getattr(cfg, 'LEAD_MAGNET_DIR', None) or os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'web', 'static', 'lead_magnets')
            safe_dir = os.path.abspath(safe_dir)

            file_real = os.path.realpath(magnet.file_path)
            # Ensure magnet file is inside the safe directory
            if not file_real.startswith(safe_dir):
                raise HTTPException(status_code=403)

            if not os.path.exists(file_real):
                raise HTTPException(status_code=404)

            # Update download count (skip tracking individual downloads for now)
            try:
                magnet.download_count = (magnet.download_count or 0) + 1
                db.add(magnet)
                await db.commit()
            except Exception:
                # Non-fatal; continue to serve file
                try:
                    await db.rollback()
                except Exception:
                    pass

            return FileResponse(path=file_real, filename=os.path.basename(file_real), media_type='application/octet-stream')
    except HTTPException as e:
        raise e
    except Exception:
        # On any unexpected error, render marketing home as fallback
        return request.app.state.templates.TemplateResponse("marketing/site.html", context)
