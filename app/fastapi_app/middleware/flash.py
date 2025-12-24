# app/fastapi_app/middleware/flash.py

import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Awaitable
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from itsdangerous import URLSafeSerializer

class FlashMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, secret_key: str, cookie_name: str = "flash_messages"):
        super().__init__(app)
        self.serializer = URLSafeSerializer(secret_key, salt="flash-messages")
        self.cookie_name = cookie_name

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Load flashed messages from cookie
        flashed_messages = []
        if self.cookie_name in request.cookies:
            try:
                data = self.serializer.loads(request.cookies[self.cookie_name])
                flashed_messages = json.loads(data)
            except Exception:
                flashed_messages = []
        
        request.state.flashed_messages = flashed_messages
        request.state.new_flashes = []

        response = await call_next(request)

        # If there are new flashes, set the cookie
        if request.state.new_flashes:
            data = json.dumps(request.state.new_flashes)
            response.set_cookie(
                self.cookie_name,
                self.serializer.dumps(data),
                httponly=True,
                samesite="lax",
                secure=True, # Recommend secure in production
            )
        # If messages were consumed (request.state.flashed_messages is empty) and there are no new flashes, clear the cookie
        elif not request.state.flashed_messages and not request.state.new_flashes and self.cookie_name in request.cookies:
            response.delete_cookie(self.cookie_name)

        return response

def flash(request: Request, message: str, category: str = "message"):
    """
    Adds a flash message to the session.
    """
    if not hasattr(request.state, "new_flashes"):
        request.state.new_flashes = []
    request.state.new_flashes.append({"message": message, "category": category})

def get_flashed_messages(request: Request, with_categories: bool = False):
    """
    Retrieves and clears flashed messages.
    """
    if not hasattr(request.state, "flashed_messages"):
        return []
    
    messages = request.state.flashed_messages
    request.state.flashed_messages = [] # Consume them

    if with_categories:
        return [(msg["category"], msg["message"]) for msg in messages]
    else:
        return [msg["message"] for msg in messages]
