"""
Synchronous wrappers for asynchronous handlers.
"""

import asyncio
from typing import Dict, Any

from app.handlers.breeder_handlers_async import create_breeder as async_create_breeder
from app.models_async.base import get_async_session as get_session

def sync_create_breeder(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synchronous wrapper for the async create_breeder handler.
    """
    async def run_async():
        async for session in get_session():
            return await async_create_breeder(data, session)
    
    return asyncio.run(run_async())
