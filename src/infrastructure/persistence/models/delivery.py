from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.persistence.database.connection import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_code = Column(String(50), unique=True, nullable=False, index=True)
    sender_name = Column(String(100), nullable=False)
    sender_address = Column(String(255), nullable=False)
    recipient_name = Column(String(100), nullable=False)
    recipient_address = Column(String(255), nullable=False)
    status = Column(  # type: ignore[var-annotated]
        Enum("pending", "in_transit", "delivered", "failed", "returned", name="delivery_status"),
        default="pending",
        nullable=False,
    )
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    vehicle = relationship("Vehicle", back_populates="deliveries")
    events = relationship("TrackingEvent", back_populates="delivery", order_by="TrackingEvent.occurred_at")
