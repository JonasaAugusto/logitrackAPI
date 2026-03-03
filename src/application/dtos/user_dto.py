from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["jonas_dev"])
    email: EmailStr = Field(..., examples=["jonas@example.com"])
    password: str = Field(
        ..., min_length=6, description="Senha em texto plano para ser hasheada", examples=["senha123"]
    )


class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
