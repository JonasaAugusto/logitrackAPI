import fastapi_swagger_dark as fsd
from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from ..cache import get_redis
from ..config.logging import setup_logging
from ..config.settings import settings
from ..persistence.database.connection import get_db
from ..persistence.models.delivery import Delivery
from ..persistence.models.user import User
from ..persistence.models.vehicle import Vehicle
from .middleware.rate_limit import RateLimitMiddleware
from .routers.auth import router as auth_router
from .routers.deliveries import router as deliveries_router
from .routers.tracking import router as tracking_router
from .routers.users import router as users_router

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME, docs_url=None, redoc_url="/redocs", openapi_url="/openapi.json")
docs_router = APIRouter()
fsd.install(docs_router)

app.include_router(docs_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(deliveries_router)
app.include_router(tracking_router)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
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


@app.get("/metrics", tags=["Health"])
async def metrics(db: AsyncSession = Depends(get_db)):
    users_total = (await db.execute(select(func.count()).select_from(User))).scalar() or 0
    users_active = (
        await db.execute(select(func.count()).select_from(User).where(User.is_active == True))  # noqa: E712
    ).scalar() or 0

    deliveries_total = (await db.execute(select(func.count()).select_from(Delivery))).scalar() or 0
    by_status: dict[str, int] = {}
    for s in ("pending", "in_transit", "delivered", "failed", "returned"):
        by_status[s] = (
            await db.execute(select(func.count()).select_from(Delivery).where(Delivery.status == s))  # type: ignore[arg-type]
        ).scalar() or 0

    vehicles_total = (await db.execute(select(func.count()).select_from(Vehicle))).scalar() or 0
    vehicles_active = (
        await db.execute(select(func.count()).select_from(Vehicle).where(Vehicle.is_active == True))  # noqa: E712
    ).scalar() or 0

    return {
        "users": {"total": users_total, "active": users_active},
        "deliveries": {"total": deliveries_total, "by_status": by_status},
        "vehicles": {"total": vehicles_total, "active": vehicles_active},
    }
