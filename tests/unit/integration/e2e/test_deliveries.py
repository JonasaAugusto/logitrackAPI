from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_vehicles_returns_empty(client: AsyncClient, mock_db_session):
    resp = await client.get("/vehicles/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_deliveries_returns_empty(client: AsyncClient, mock_db_session):
    resp = await client.get("/deliveries/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_get_vehicle_not_found(client: AsyncClient, mock_db_session):
    mock_db_session._scalar_return_value = None
    resp = await client.get("/vehicles/9999")
    assert resp.status_code == 404
    assert "não encontrado" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_delivery_not_found(client: AsyncClient, mock_db_session):
    mock_db_session._scalar_return_value = None
    resp = await client.get("/deliveries/LTNOTFOUND")
    assert resp.status_code == 404
    assert "não encontrada" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_vehicle_invalid_plate_too_short(client: AsyncClient):
    resp = await client.post(
        "/vehicles/",
        json={"plate": "AB", "model": "Fiat Ducato", "type": "van", "driver_name": "João Silva"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_vehicle_invalid_type(client: AsyncClient):
    resp = await client.post(
        "/vehicles/",
        json={"plate": "ABC-1234", "model": "Fiat Ducato", "type": "bicycle", "driver_name": "João"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_delivery_missing_required_fields(client: AsyncClient):
    resp = await client.post("/deliveries/", json={"sender_name": "Só o remetente"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_delivery_with_nonexistent_vehicle(client: AsyncClient, mock_db_session):
    mock_db_session._scalar_return_value = None
    resp = await client.post(
        "/deliveries/",
        json={
            "sender_name": "Empresa ABC",
            "sender_address": "Rua A, 100",
            "recipient_name": "João Silva",
            "recipient_address": "Rua B, 200",
            "vehicle_id": 9999,
        },
    )
    assert resp.status_code == 404
    assert "Veículo" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_metrics_endpoint(client: AsyncClient, mock_db_session):
    mock_result = MagicMock()
    mock_result.scalar.return_value = 0
    mock_db_session.execute.side_effect = None
    mock_db_session.execute.return_value = mock_result

    resp = await client.get("/metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert "users" in data
    assert "deliveries" in data
    assert "vehicles" in data
    assert "by_status" in data["deliveries"]
    assert "total" in data["users"]
    assert "active" in data["users"]
