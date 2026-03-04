import fastapi_swagger_dark as fsd
from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..cache import get_redis
from ..config.settings import settings
from ..persistence.database.connection import get_db
from .routers.auth import router as auth_router
from .routers.tracking import router as tracking_router
from .routers.users import router as users_router

app = FastAPI(title=settings.PROJECT_NAME, docs_url=None, redoc_url="/redocs", openapi_url="/openapi.json")
docs_router = APIRouter()
fsd.install(docs_router)

app.include_router(docs_router)
app.include_router(users_router)
app.include_router(tracking_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Server is running!"}


@app.get("/health", tags=["Health"])
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
):
    await db.execute(text("SELECT 1"))

    await redis_client.ping()  # type: ignore

    return {
        "status": "ok",
        "database": "connected",
        "redis": "connected",
    }
