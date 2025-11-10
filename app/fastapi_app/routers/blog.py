"""
Blog API Router - Pure JSON CRUD operations
RESTful API endpoints under /api/v1/blog with Pydantic contracts
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.fastapi_app.dependencies import get_current_user, get_current_admin_user
from app.models_async.auth import User
from app.models_async.blog import Post, Category
from app.models_async.base import get_async_session
from app.fastapi_app.models.blog import PostCreate, PostUpdate, PostResponse, PostListResponse

router = APIRouter(tags=["blog"])

@router.get("/", response_model=PostListResponse)
async def list_posts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    category_id: Optional[int] = Query(None, ge=1, description="Filter by category ID"),
    author_id: Optional[int] = Query(None, ge=1, description="Filter by author ID"),
    search: Optional[str] = Query(None, description="Search in post titles and content"),
    db: AsyncSession = Depends(get_async_session),
):
    """Get paginated list of blog posts"""
    query = select(Post).where(Post.is_published == True)
    count_query = select(func.count(Post.id)).where(Post.is_published == True)

    if category_id:
        query = query.where(Post.category_id == category_id)
        count_query = count_query.where(Post.category_id == category_id)
    
    if author_id:
        query = query.where(Post.author_id == author_id)
        count_query = count_query.where(Post.author_id == author_id)

    if search:
        query = query.where(Post.title.ilike(f"%{search}%") | Post.content.ilike(f"%{search}%"))
        count_query = count_query.where(Post.title.ilike(f"%{search}%") | Post.content.ilike(f"%{search}%"))

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    query = query.order_by(Post.published_at.desc()).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    posts = result.scalars().all()
    
    items = [PostResponse.from_orm(post) for post in posts]

    return PostListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
        has_next=page * page_size < total,
        has_prev=page > 1
    )

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new blog post"""
    new_post = Post(**post_data.dict(), author_id=current_user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return PostResponse.from_orm(new_post)

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get a single blog post by ID"""
    post = await db.get(Post, post_id)
    if not post or not post.is_published:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponse.from_orm(post)

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a blog post"""
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
        
    await db.commit()
    await db.refresh(post)
    return PostResponse.from_orm(post)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a blog post"""
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await db.delete(post)
    await db.commit()
    return None
