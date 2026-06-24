import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_returns_ok(client: AsyncClient):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Server is running!"


@pytest.mark.asyncio
async def test_list_users_requires_auth():
    from httpx import ASGITransport, AsyncClient

    from src.infrastructure.api.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/users/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_create_user_invalid_email(client: AsyncClient):
    resp = await client.post(
        "/users/",
        json={
            "username": "validuser",
            "email": "not-an-email",
            "password": "senha123",
        },
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_user_missing_fields(client: AsyncClient):
    resp = await client.post("/users/", json={"username": "onlyname"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_update_user_extra_field_rejected(client: AsyncClient, mock_db_session, mock_user_factory):
    mock_db_session._scalar_return_value = mock_user_factory()

    resp = await client.patch("/users/1", json={"unknown_field": "value"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient, mock_db_session):
    mock_db_session._scalar_return_value = None

    resp = await client.get("/users/99999")
    assert resp.status_code == 404
