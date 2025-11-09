"""
Flask-compatible async helpers for async SQLAlchemy operations.

This module provides utilities to bridge Flask's synchronous request handling
with async SQLAlchemy database operations.
"""

import asyncio
from typing import Any, AsyncGenerator, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.logger import logger
from app.models_async.base import AsyncSessionLocal, async_engine

# Global async session factory (matches models_async configuration)
_async_session_factory = AsyncSessionLocal


async def get_flask_async_session() -> AsyncSession:
    """
    Create an async session for Flask route handlers.

    This function creates a new async session that can be used in Flask route
    handlers. The caller is responsible for closing the session.

    Usage in Flask routes:
    ```python
    session = await get_flask_async_session()
    try:
        result = await some_async_handler(session)
        return jsonify({"success": True, "data": result})
    finally:
        await session.close()
    ```

    Returns:
        AsyncSession: A new async database session
    """
    session = _async_session_factory()
    return session


async def execute_async_handler_with_session(
    handler_func, *handler_args, **handler_kwargs
) -> Any:
    """
    Execute an async handler function with proper session management.

    This function:
    1. Creates a new async session
    2. Passes it to the handler function
    3. Handles session lifecycle (close/rollback on error)
    4. Returns the result
    NO AUTO-COMMIT: Caller must explicitly commit

    Args:
        handler_func: Async function to execute (receives session as first arg)
        *handler_args: Additional arguments to pass to handler
        **handler_kwargs: Additional keyword arguments to pass to handler

    Returns:
        Any: Result from the handler function

    Example:
    ```python
    result = await execute_async_handler_with_session(
        get_all_plants_async,
        current_user_id=1
    )
    ```
    """
    session = _async_session_factory()
    try:
        # Add session as first argument if not already provided
        if handler_args:
            # Session should already be first argument
            result = await handler_func(*handler_args, **handler_kwargs)
        else:
            # Add session as first argument
            result = await handler_func(session, **handler_kwargs)

        # NO AUTO-COMMIT: Caller must explicitly commit
        return result
    except Exception as e:
        await session.rollback()
        logger.error(f"Error in async handler execution: {e}")
        raise
    finally:
        await session.close()


async def execute_async_with_session_context(
    handler_func, session: AsyncSession, *handler_args, **handler_kwargs
) -> Any:
    """
    Execute an async handler function with an existing session.

    This function assumes the session is already created and managed
    externally (e.g., in async for loop). It just executes the handler
    and handles errors.

    Args:
        handler_func: Async function to execute
        session: Existing AsyncSession to use
        *handler_args: Additional arguments to pass to handler
        **handler_kwargs: Additional keyword arguments to pass to handler

    Returns:
        Any: Result from the handler function
    """
    try:
        result = await handler_func(session, *handler_args, **handler_kwargs)
        return result
    except Exception as e:
        logger.error(f"Error in async handler execution: {e}")
        await session.rollback()
        raise


class FlaskAsyncSessionManager:
    """
    Context manager for async sessions in Flask routes.

    This provides a cleaner interface for Flask routes to use async
    database operations while maintaining proper session lifecycle.

    Usage:
    ```python
    @app.route('/api/plants')
    async def get_plants():
        async with FlaskAsyncSessionManager() as session:
            plants = await get_all_plants_async(session)
            return jsonify(plants)
    ```
    """

    def __init__(self):
        self.session = None

    async def __aenter__(self) -> AsyncSession:
        self.session = _async_session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        NO AUTO-COMMIT: Close session without auto-committing.
        Caller must explicitly commit before exiting.
        """
        if exc_type is not None:
            # Exception occurred - rollback
            await self.session.rollback()
            logger.warning(
                "Session rolled back due to exception in FlaskAsyncSessionManager"
            )
        # Always close session, but no auto-commit
        await self.session.close()


# Convenience aliases for backward compatibility
get_async_db_session = get_flask_async_session
with_async_session = FlaskAsyncSessionManager
