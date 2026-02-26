from typing import AsyncGenerator

from redis.asyncio import Redis


async def get_redis() -> AsyncGenerator[Redis, None]:
    redis = Redis(
        host="redis",
        port=6379,
        decode_responses=True,
    )
    try:
        yield redis
    finally:
        await redis.close()
