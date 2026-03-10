import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user_200(client: AsyncClient, mock_db_session, mock_user_factory):
    """Testa obtenção de usuário existente"""
    mock_user = mock_user_factory(
        user_id=1,
        email="test@logitrack.com",
        name="Test User",
        username="testuser",
        is_active=True,
    )
    mock_db_session._scalar_return_value = mock_user

    resp = await client.get("/users/1")

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["email"] == "test@logitrack.com"


@pytest.mark.asyncio
async def test_get_user_404(client: AsyncClient, mock_db_session):
    """Testa obtenção de usuário inexistente"""
    mock_db_session._scalar_return_value = None

    resp = await client.get("/users/999999")

    assert resp.status_code == 404
