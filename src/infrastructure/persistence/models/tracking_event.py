from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.persistence.database.connection import Base


class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.id"), nullable=False, index=True)
    status = Column(  # type: ignore[var-annotated]
        Enum("pending", "in_transit", "delivered", "failed", "returned", name="delivery_status"),
        nullable=False,
    )
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())

    delivery = relationship("Delivery", back_populates="events")
