import time
from functools import wraps
from fastapi import Request, HTTPException, status
import redis

# Redis client for rate limiting
# TODO: Configure Redis connection from environment variables
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def rate_limit(limit: int, window: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Get client IP (support proxy)
            forwarded = request.headers.get("X-Forwarded-For")
            if forwarded:
                client_ip = forwarded.split(",")[0].strip()
            else:
                client_ip = request.client.host if request.client else "unknown"

            try:
                # Use Redis for rate limiting
                current_time = int(time.time())
                key = f"rate_limit:{func.__name__}:{client_ip}"
                
                # Use a transaction to ensure atomicity
                pipe = redis_client.pipeline()
                pipe.zremrangebyscore(key, 0, current_time - window)
                pipe.zadd(key, {current_time: current_time})
                pipe.zcard(key)
                pipe.expire(key, window)
                results = pipe.execute()

                count = results[2]

                if count > limit:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"Rate limit exceeded. Try again in {window} seconds.",
                    )
                
                return await func(request, *args, **kwargs)
            except redis.exceptions.ConnectionError:
                # Fallback to no rate limiting if Redis is not available
                return await func(request, *args, **kwargs)
        return wrapper
    return decorator
