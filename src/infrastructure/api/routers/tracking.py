from fastapi import APIRouter, HTTPException

from src.infrastructure.external.tracking_service import get_external_tracking

router = APIRouter(prefix="/tracking", tags=["Tracking"])


@router.get("/")
async def get_tracking():
    return {"message": "Endpoint de rastreamento ativo. Use /external/{tracking_number} para consultar."}


@router.get("/external/{tracking_number}", summary="Consulta rastreamento em API externa")
async def track_external(tracking_number: str):
    try:
        data = await get_external_tracking(tracking_number)
        return {"tracking_number": tracking_number, "status": "success", "external_data": data}
    except HTTPException as e:
        raise e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao consultar rastreamento: {str(exc)}")
