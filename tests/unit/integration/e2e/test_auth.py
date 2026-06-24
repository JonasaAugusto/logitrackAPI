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
