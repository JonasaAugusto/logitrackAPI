from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dtos.user_dto import (  # UserUpdateDTO,; UserListItemDTO
    UserCreateDTO,
    UserResponseDTO,
)
from src.infrastructure.persistence.database.connection import get_db
from src.infrastructure.persistence.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)


@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreateDTO, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado")

    result = await db.execute(select(User).where(User.username == user_in.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já registrado")

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        is_active=True,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
