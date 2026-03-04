import httpx
from fastapi import HTTPException

from src.infrastructure.config.settings import settings


async def get_external_tracking(tracking_number: str) -> dict:
    """
    Consulta rastreamento via PacoteVício (RapidAPI).
    Endpoint: /track (Rastrear Qualquer Encomenda)
    Limite free: 1.000 req/mês
    """
    url = f"{settings.EXTERNAL_API_BASE_URL}/track"

    headers: dict[str, str] = {
        "X-RapidAPI-Key": str(settings.EXTERNAL_API_KEY or ""),
        "X-RapidAPI-Host": str(settings.EXTERNAL_API_HOST or ""),
        "Content-Type": "application/json",
    }

    params = {"tracking_code": tracking_number, "confidence_level": "high"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data

        except httpx.TimeoutException:
            raise HTTPException(504, "Tempo esgotado (confidence_level high pode demorar até 30s)")
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            detail = e.response.json().get("message", "Erro na API do PacoteVício")
            raise HTTPException(status_code=status_code, detail=detail)
        except httpx.RequestError as e:
            raise HTTPException(503, f"Erro de conexão com PacoteVício: {str(e)}")
        except Exception as e:
            raise HTTPException(500, f"Erro inesperado: {str(e)}")
