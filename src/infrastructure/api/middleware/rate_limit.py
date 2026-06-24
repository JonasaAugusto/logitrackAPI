from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.infrastructure.cache import get_redis_client

RATE_LIMIT = 100
WINDOW_SECONDS = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate:{client_ip}"

        try:
            redis = await get_redis_client()
            count = await redis.incr(key)
            if count == 1:
                await redis.expire(key, WINDOW_SECONDS)

            if count > RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={"detail": f"Limite de {RATE_LIMIT} requisições por minuto atingido"},
                    headers={"Retry-After": str(WINDOW_SECONDS)},
                )
        except Exception:
            pass

        return await call_next(request)
