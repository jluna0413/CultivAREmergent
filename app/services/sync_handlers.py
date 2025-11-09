"""
Synchronous wrappers for asynchronous handlers.
"""

import asyncio
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.breeder_handlers_async import create_breeder as async_create_breeder
from app.models_async.base import get_async_session

def sync_create_breeder(breeder_data: dict, session: 'AsyncSession' = None):
    """
    Synchronous wrapper for the async create_breeder handler.
    """
    if session is None:
        session_generator = get_async_session()
        session = asyncio.run(session_generator.__anext__())
    
    return asyncio.run(async_create_breeder(breeder_data, session))
