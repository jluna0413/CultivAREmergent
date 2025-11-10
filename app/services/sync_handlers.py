"""
Synchronous wrappers for asynchronous handlers.
"""

import asyncio
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.breeder_handlers_async import create_breeder as async_create_breeder
from app.models_async.base import get_async_session

def sync_create_breeder(breeder_data: dict, session: 'AsyncSession' = None, user_id: int = None):
    """
    Synchronous wrapper for the async create_breeder handler.

    Ensures optional `user_id` injection is honored by adding it to the
    breeder_data payload if provided. If no session is passed, one is
    obtained from the async session generator.
    """
    # Inject user_id into the data payload if provided and not already set
    if user_id is not None and breeder_data.get("user_id") is None:
        breeder_data["user_id"] = user_id

    # Acquire an AsyncSession if not passed in
    if session is None:
        session_generator = get_async_session()
        session = asyncio.run(session_generator.__anext__())

    # Call the async handler synchronously
    return asyncio.run(async_create_breeder(breeder_data, session))