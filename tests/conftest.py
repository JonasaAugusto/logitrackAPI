# conftest.py
import asyncio
import sys
import warnings
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.api.dependencies import get_current_user
from src.infrastructure.api.main import app
from src.infrastructure.cache import get_redis
from src.infrastructure.persistence.database.connection import get_db
from src.infrastructure.persistence.models.user import User

if sys.platform == "win32":
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore[attr-defined]


async def mocked_get_current_user():
    return {"id": 1, "email": "test@logitrack.com"}


@pytest.fixture(scope="function")
async def client():
    app.dependency_overrides[get_current_user] = mocked_get_current_user
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def mock_user_factory():
    """Factory para criar usuários mockados com TODOS os campos exigidos pelo schema"""

    def _create_user(
        user_id: int = 1,
        email: str = "test@logitrack.com",
        name: str = "Test User",
        username: str = "testuser",
        is_active: bool = True,
        created_at: datetime | None = None,
    ):
        user = Mock(spec=User)
        user.id = user_id
        user.email = email
        user.name = name
        user.username = username
        user.is_active = is_active
        user.created_at = created_at or datetime.now(timezone.utc)
        return user

    return _create_user


@pytest.fixture
def mock_db_session(mock_user_factory):
    """Mock de sessão SQLAlchemy com retorno configurável"""
    mock_session = AsyncMock(spec=AsyncSession)

    mock_session._scalar_return_value = None

    def mock_execute_side_effect(query, *args, **kwargs):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_session._scalar_return_value
        mock_result.scalars.return_value.all.return_value = []
        return mock_result

    mock_session.execute.side_effect = mock_execute_side_effect
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.refresh = AsyncMock()

    return mock_session


@pytest.fixture(autouse=True)
def override_database_dependencies(mock_db_session):
    """Substitui get_db e get_redis por mocks"""

    async def mock_get_db():
        yield mock_db_session

    mock_redis = AsyncMock()
    mock_redis.ping = AsyncMock(return_value=True)
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)

    async def mock_get_redis():
        return mock_redis

    app.dependency_overrides[get_db] = mock_get_db
    app.dependency_overrides[get_redis] = mock_get_redis

    yield

    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_redis, None)
