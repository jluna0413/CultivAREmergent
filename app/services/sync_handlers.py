"""
Synchronous wrappers for asynchronous handlers.
"""

import asyncio
from typing import Dict, Any, Optional

from app.handlers.breeder_handlers_async import create_breeder as async_create_breeder
from app.models_async.base import get_async_session as get_session

def sync_create_breeder(data: Dict[str, Any], session: Optional[Any] = None) -> Dict[str, Any]:
    """
    Synchronous wrapper for the async create_breeder handler.
    """
    async def run_async():
        if session:
            return await async_create_breeder(data, session)
        else:
            async for new_session in get_session():
                return await async_create_breeder(data, new_session)
    
    return asyncio.run(run_async())
