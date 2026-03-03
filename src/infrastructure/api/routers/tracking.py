from fastapi import APIRouter

router = APIRouter(prefix="/tracking", tags=["Tracking"])


@router.get("/")
async def get_tracking():
    return {"message": "Tracking endpoint placeholder"}


# @router.get("/external/{tracking_number}")
# async def track_external(tracking_number: str):
# data = await get_external_tracking(tracking_number)
# return {"external_data": data}
