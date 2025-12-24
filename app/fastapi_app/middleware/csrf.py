# app/fastapi_app/middleware/csrf.py

import secrets
from itsdangerous import URLSafeSerializer, BadSignature
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable, Optional, List
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.types import ASGIApp

class CSRFMiddleware(BaseHTTPMiddleware):
    """
    CSRF protection middleware for FastAPI.
    A replacement for Flask-WTF CSRFProtect.
    """
    def __init__(self, app: ASGIApp, secret: str, cookie_name: str = "csrf_token", header_name: str = "X-CSRF-Token", safe_methods: set = {"GET", "HEAD", "OPTIONS"}, exclude_paths: Optional[List[str]] = None):
        super().__init__(app)
        self.serializer = URLSafeSerializer(secret, salt="csrf-token")
        self.secret = secret
        self.cookie_name = cookie_name
        self.header_name = header_name
        self.safe_methods = safe_methods
        self.exclude_paths = exclude_paths if exclude_paths is not None else []

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Exclude paths from CSRF protection
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        csrf_token_from_cookie = request.cookies.get(self.cookie_name)
        new_csrf_raw_token = None
        
        if csrf_token_from_cookie:
            try:
                # Attempt to load the token from the cookie
                request.state.csrf_raw_token = self.serializer.loads(csrf_token_from_cookie)
            except BadSignature:
                # If signature is bad, generate a new token
                new_csrf_raw_token = secrets.token_hex(16)
                request.state.csrf_raw_token = new_csrf_raw_token
        else:
            # If no cookie, generate a new token
            new_csrf_raw_token = secrets.token_hex(16)
            request.state.csrf_raw_token = new_csrf_raw_token

        # Store the serialized token for later use (e.g., in templates)
        request.state.csrf_token = self.serializer.dumps(request.state.csrf_raw_token)

        if request.method not in self.safe_methods:
            # Validate token
            header_token = request.headers.get(self.header_name)
            
            sent_token = None
            if header_token:
                sent_token = header_token
            elif request.headers.get("content-type", "").startswith(("application/x-www-form-urlencoded", "multipart/form-data")):
                form_data = await request.form()
                sent_token = form_data.get("csrf_token")
            
            if not sent_token:
                return JSONResponse(status_code=403, content={"detail": "CSRF token missing"})

            try:
                # Compare the sent token with the one from the cookie
                if self.serializer.loads(sent_token) != request.state.csrf_raw_token:
                    return JSONResponse(status_code=403, content={"detail": "Invalid CSRF token"})
            except BadSignature:
                return JSONResponse(status_code=403, content={"detail": "Invalid CSRF token"})

        response = await call_next(request)

        # Always set the cookie if a new token was generated or if it was missing/invalid
        if new_csrf_raw_token or not csrf_token_from_cookie:
             response.set_cookie(
                self.cookie_name,
                request.state.csrf_token, # Store the serialized token in the cookie
                httponly=True,
                samesite="lax",
                secure=True, # Recommend secure in production
            )
        
        return response

def generate_csrf_token(request: Request) -> str:
    """
    Function to be used in templates to get the raw CSRF token.
    """
    return request.state.csrf_raw_token
