from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.persistence.database.connection import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plate = Column(String(10), unique=True, nullable=False, index=True)
    model = Column(String(100), nullable=False)
    type = Column(Enum("truck", "van", "motorcycle", "car", name="vehicle_type"), nullable=False)  # type: ignore[var-annotated]
    driver_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    deliveries = relationship("Delivery", back_populates="vehicle")
