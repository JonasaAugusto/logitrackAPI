# async def get_external_tracking(tracking_number: str):
# async with httpx.AsyncClient(timeout=10.0) as client:
# try:
# resp = await client.get(
#    f"https://external-api.com/track/{tracking_number}", headers={"X-API-Key": settings.EXTERNAL_API_KEY}
# )
# resp.raise_for_status()
# return resp.json()
# except httpx.HTTPStatusError as e:
# raise HTTPException(status_code=e.response.status_code, detail="API externa falhou")
# except httpx.RequestError:
# raise HTTPException(status_code=503, detail="Serviço externo indisponível")
