import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, mock_db_session, mock_user_factory):
    from datetime import datetime, timezone
    from unittest.mock import AsyncMock

    mock_db_session._scalar_return_value = None

    def set_defaults(obj):
        obj.id = 1
        obj.created_at = datetime.now(timezone.utc)

    mock_db_session.refresh = AsyncMock(side_effect=set_defaults)

    resp = await client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "new@test.com",
            "password": "senha123",
        },
    )

    assert resp.status_code == 201


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, mock_db_session, mock_user_factory):
    existing_user = mock_user_factory(email="existing@test.com")
    mock_db_session._scalar_return_value = existing_user

    resp = await client.post(
        "/auth/register",
        json={
            "username": "anyuser",
            "email": "existing@test.com",
            "password": "senha123",
        },
    )

    assert resp.status_code == 400
    assert "Email" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_register_short_password(client: AsyncClient):
    resp = await client.post(
        "/auth/register",
        json={
            "username": "validuser",
            "email": "valid@test.com",
            "password": "123",
        },
    )

    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_login_wrong_credentials(client: AsyncClient, mock_db_session):
    mock_db_session._scalar_return_value = None

    resp = await client.post(
        "/auth/login",
        data={
            "username": "ninguem",
            "password": "errado",
        },
    )

    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, mock_db_session, mock_user_factory):
    from src.infrastructure.config.auth import hash_password

    hashed = hash_password("senha123")
    mock_user = mock_user_factory(username="testuser", email="test@logitrack.com")
    mock_user.password_hash = hashed
    mock_db_session._scalar_return_value = mock_user

    resp = await client.post(
        "/auth/login",
        data={"username": "testuser", "password": "senha123"},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient):
    from src.infrastructure.config.auth import create_refresh_token

    token = create_refresh_token(data={"sub": "testuser"})
    resp = await client.post("/auth/logout", json={"token": token})
    assert resp.status_code == 204
