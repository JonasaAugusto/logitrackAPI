from fastapi import APIRouter

router = APIRouter(prefix="/tracking", tags=["tracking"])

@router.get("/")
def list_tracking():
    return [{"id": 1, "status": "in transit"}, {"id": 2, "status": "delivered"}]
