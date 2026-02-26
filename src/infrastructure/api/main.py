from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from infrastructure.api.routers import users, tracking
from infrastructure.cache import get_redis
from infrastructure.database import get_db
from infrastructure.config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users.router)
app.include_router(tracking.router)


@app.get("/")
def root():
    return {"message": "Server is running!"}


@app.get("/health", tags=["Health"])
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
):
    """
    Verifica a conectividade com o Banco de Dados e o Redis.
    """
    await db.execute(text("SELECT 1"))
    await redis_client.ping()  # type: ignore

    return {
        "status": "ok",
        "database": "connected",
        "redis": "connected",
    }
