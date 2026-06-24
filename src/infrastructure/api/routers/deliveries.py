import secrets
import string
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.application.dtos.delivery_dto import (
    DeliveryCreateDTO,
    DeliveryResponseDTO,
    DeliveryUpdateDTO,
    VehicleCreateDTO,
    VehicleResponseDTO,
)
from src.infrastructure.config.auth import TokenData, get_current_user
from src.infrastructure.persistence.database.connection import get_db
from src.infrastructure.persistence.models.delivery import Delivery
from src.infrastructure.persistence.models.tracking_event import TrackingEvent
from src.infrastructure.persistence.models.vehicle import Vehicle

router = APIRouter(tags=["Deliveries"])


def _generate_tracking_code() -> str:
    chars = string.ascii_uppercase + string.digits
    return "LT" + "".join(secrets.choice(chars) for _ in range(10))


# ── Vehicles ──────────────────────────────────────────────────────────────────


@router.post("/vehicles/", response_model=VehicleResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_in: VehicleCreateDTO,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    existing = await db.execute(select(Vehicle).where(Vehicle.plate == vehicle_in.plate))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Veículo com essa placa já existe")

    vehicle = Vehicle(**vehicle_in.model_dump())
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


@router.get("/vehicles/", response_model=List[VehicleResponseDTO])
async def list_vehicles(
    skip: int = 0,
    limit: int = 50,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Vehicle).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponseDTO)
async def get_vehicle(
    vehicle_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    vehicle = result.scalar_one_or_none()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return vehicle


# ── Deliveries ─────────────────────────────────────────────────────────────────


@router.post("/deliveries/", response_model=DeliveryResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_delivery(
    delivery_in: DeliveryCreateDTO,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if delivery_in.vehicle_id:
        result = await db.execute(select(Vehicle).where(Vehicle.id == delivery_in.vehicle_id))
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Veículo não encontrado")

    tracking_code = _generate_tracking_code()
    delivery = Delivery(tracking_code=tracking_code, **delivery_in.model_dump())
    db.add(delivery)

    event = TrackingEvent(delivery=delivery, status="pending", description="Entrega criada")
    db.add(event)

    await db.commit()
    await db.refresh(delivery)

    result = await db.execute(select(Delivery).where(Delivery.id == delivery.id).options(selectinload(Delivery.events)))
    return result.scalar_one()


@router.get("/deliveries/", response_model=List[DeliveryResponseDTO])
async def list_deliveries(
    skip: int = 0,
    limit: int = 50,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Delivery).options(selectinload(Delivery.events)).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/deliveries/{tracking_code}", response_model=DeliveryResponseDTO)
async def get_delivery(
    tracking_code: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Delivery).where(Delivery.tracking_code == tracking_code).options(selectinload(Delivery.events))
    )
    delivery = result.scalar_one_or_none()
    if not delivery:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return delivery


@router.patch("/deliveries/{tracking_code}", response_model=DeliveryResponseDTO)
async def update_delivery(
    tracking_code: str,
    update_in: DeliveryUpdateDTO,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Delivery).where(Delivery.tracking_code == tracking_code).options(selectinload(Delivery.events))
    )
    delivery = result.scalar_one_or_none()
    if not delivery:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")

    update_data = update_in.model_dump(exclude_unset=True)
    location = update_data.pop("location", None)

    if "status" in update_data and update_data["status"] != delivery.status:
        event = TrackingEvent(
            delivery_id=delivery.id,
            status=update_data["status"],
            location=location,
            description=f"Status atualizado para {update_data['status']}",
        )
        db.add(event)

    for key, value in update_data.items():
        setattr(delivery, key, value)

    await db.commit()

    result = await db.execute(select(Delivery).where(Delivery.id == delivery.id).options(selectinload(Delivery.events)))
    return result.scalar_one()
