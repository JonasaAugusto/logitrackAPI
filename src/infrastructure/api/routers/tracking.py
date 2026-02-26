from fastapi import APIRouter

router = APIRouter(prefix="/tracking", tags=["Tracking"])


@router.get("/")
async def get_tracking():
    return {"message": "Tracking endpoint placeholder"}
