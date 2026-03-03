from httpx import AsyncClient


async def test_get_user_200(client: AsyncClient):
    resp = await client.get("/users/1")
    assert resp.status_code == 200


async def test_get_user_404(client: AsyncClient):
    resp = await client.get("/users/999999")
    assert resp.status_code == 404
