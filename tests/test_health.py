import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport

from infrastructure.api.main import app
from infrastructure.database import get_db
from infrastructure.cache import get_redis


@pytest.mark.asyncio
async def test_health_check_success():
    """
    Testa o endpoint /health usando mocks para Database e Redis.
    Isso evita a necessidade de containers ou serviços externos.
    """

    mock_db = AsyncMock()

    mock_redis = AsyncMock()
    mock_redis.ping.return_value = True

    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_redis] = lambda: mock_redis

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/health")

        assert response.status_code == 200

        assert response.json() == {
            "status": "ok",
            "database": "connected",
            "redis": "connected",
        }
    finally:
        app.dependency_overrides = {}