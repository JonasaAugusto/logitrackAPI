from typing import AsyncGenerator

from redis.asyncio import Redis

from src.infrastructure.config.settings import settings


def _make_redis() -> Redis:
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_redis() -> AsyncGenerator[Redis, None]:
    redis = _make_redis()
    try:
        yield redis
    finally:
        await redis.aclose()


async def get_redis_client() -> Redis:
    return _make_redis()
