import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dtos.user_dto import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from src.application.use_cases.create_user import CreateUserUseCase
from src.application.use_cases.delete_user import DeleteUserUseCase
from src.application.use_cases.get_user import GetUserUseCase, ListUsersUseCase
from src.application.use_cases.update_user import UpdateUserUseCase
from src.core.exceptions.user_exceptions import (
    UnauthorizedError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.infrastructure.cache import get_redis
from src.infrastructure.config.auth import TokenData, get_current_user
from src.infrastructure.config.logging import get_logger
from src.infrastructure.persistence.database.connection import get_db
from src.infrastructure.persistence.repositories.user_repository_impl import UserRepositoryImpl

USER_CACHE_TTL = 300
logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreateDTO, db: AsyncSession = Depends(get_db)):
    try:
        repo = UserRepositoryImpl(db)
        entity = await CreateUserUseCase(repo).execute(user_in)
        logger.info("user_created", username=entity.username, user_id=entity.id)
        return entity
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("user_creation_error", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao processar o cadastro")


@router.get("/", response_model=List[UserResponseDTO])
async def list_users(
    skip: int = 0,
    limit: int = 50,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepositoryImpl(db)
    return await ListUsersUseCase(repo).execute(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    cache_key = f"user:{user_id}"
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    try:
        repo = UserRepositoryImpl(db)
        user = await GetUserUseCase(repo).execute(user_id)
        dto = UserResponseDTO.model_validate(user)
        await redis.set(cache_key, dto.model_dump_json(), ex=USER_CACHE_TTL)
        return dto
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: int,
    user_update: UserUpdateDTO,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    try:
        repo = UserRepositoryImpl(db)
        user = await UpdateUserUseCase(repo).execute(user_id, user_update)
        await redis.delete(f"user:{user_id}")
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=dict)
async def delete_user(
    user_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    try:
        if not current_user.username:
            raise HTTPException(status_code=401, detail="Não autorizado")
        repo = UserRepositoryImpl(db)
        result = await DeleteUserUseCase(repo).execute(user_id, current_user.username)
        await redis.delete(f"user:{user_id}")
        return result
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
