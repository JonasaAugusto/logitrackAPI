import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dtos.user_dto import (
    UserCreateDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from src.infrastructure.api.dependencies import TokenData, get_current_user
from src.infrastructure.persistence.database.connection import get_db
from src.infrastructure.persistence.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)


@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreateDTO, db: AsyncSession = Depends(get_db)):
    """Cria um novo usuário com validação de unicidade e logs de erro."""
    try:
        logger.info(f"Tentativa de criação de usuário: {user_in.email}")
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.scalar_one_or_none():
            logger.warning(f"Falha ao criar usuário: Email {user_in.email} já existe.")
            raise HTTPException(status_code=400, detail="Email já registrado")

        result = await db.execute(select(User).where(User.username == user_in.username))
        if result.scalar_one_or_none():
            logger.warning(f"Falha ao criar usuário: Username {user_in.username} já existe.")
            raise HTTPException(status_code=400, detail="Username já registrado")

        new_user = User(
            username=user_in.username,
            email=user_in.email,
            password_hash=hash_password(user_in.password),
            is_active=True,
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        logger.info(f"Usuário {new_user.username} criado com sucesso (ID: {new_user.id})")
        return new_user

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"ERRO CRÍTICO no registro: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar o cadastro no banco de dados",
        )


@router.get("/", response_model=List[UserResponseDTO])
async def list_users(current_user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: int, current_user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.patch("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: int,
    user_update: UserUpdateDTO,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    if "email" in update_data and update_data["email"] != user.email:
        check = await db.execute(select(User).where(User.email == update_data["email"]))
        if check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email já em uso")

    if "username" in update_data and update_data["username"] != user.username:
        check = await db.execute(select(User).where(User.username == update_data["username"]))
        if check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username já em uso")

    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=dict)
async def delete_user(
    user_id: int, current_user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if current_user.username != user.username:
        raise HTTPException(403, "Não autorizado a deletar este usuário")

    username = user.username
    await db.delete(user)
    await db.commit()

    return {"message": "Usuário deletado com sucesso", "deleted_id": user_id, "deleted_username": username}
