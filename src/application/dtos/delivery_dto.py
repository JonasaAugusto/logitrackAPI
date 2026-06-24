from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

DeliveryStatus = Literal["pending", "in_transit", "delivered", "failed", "returned"]
VehicleType = Literal["truck", "van", "motorcycle", "car"]


class VehicleCreateDTO(BaseModel):
    plate: str = Field(..., min_length=7, max_length=10, examples=["ABC-1234"])
    model: str = Field(..., min_length=2, max_length=100, examples=["Fiat Ducato"])
    type: VehicleType
    driver_name: str = Field(..., min_length=2, max_length=100, examples=["João Silva"])


class VehicleResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    plate: str
    model: str
    type: str
    driver_name: str
    is_active: bool
    created_at: datetime


class DeliveryCreateDTO(BaseModel):
    sender_name: str = Field(..., min_length=2, max_length=100)
    sender_address: str = Field(..., min_length=5, max_length=255)
    recipient_name: str = Field(..., min_length=2, max_length=100)
    recipient_address: str = Field(..., min_length=5, max_length=255)
    vehicle_id: Optional[int] = None
    notes: Optional[str] = None


class DeliveryUpdateDTO(BaseModel):
    status: Optional[DeliveryStatus] = None
    vehicle_id: Optional[int] = None
    notes: Optional[str] = None
    location: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class TrackingEventResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    location: Optional[str]
    description: Optional[str]
    occurred_at: datetime


class DeliveryResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tracking_code: str
    sender_name: str
    sender_address: str
    recipient_name: str
    recipient_address: str
    status: str
    vehicle_id: Optional[int]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    events: List[TrackingEventResponseDTO] = []
