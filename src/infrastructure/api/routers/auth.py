from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dtos.user_dto import UserCreateDTO, UserResponseDTO
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.application.use_cases.create_user import CreateUserUseCase
from src.core.exceptions.user_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from src.infrastructure.cache import get_redis
from src.infrastructure.config.auth import (
    REFRESH_TOKEN_EXPIRE_DAYS,
    Token,
    create_access_token,
    decode_refresh_token,
)
from src.infrastructure.persistence.database.connection import get_db
from src.infrastructure.persistence.repositories.user_repository_impl import UserRepositoryImpl

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreateDTO, db: AsyncSession = Depends(get_db)):
    try:
        repo = UserRepositoryImpl(db)
        return await CreateUserUseCase(repo).execute(user_in)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    try:
        repo = UserRepositoryImpl(db)
        token = await AuthenticateUserUseCase(repo).execute(form_data.username, form_data.password)
        ttl = REFRESH_TOKEN_EXPIRE_DAYS * 86400
        await redis.set(f"refresh:{form_data.username}:{token.refresh_token[-16:]}", "valid", ex=ttl)
        return token
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    username = decode_refresh_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

    key = f"refresh:{username}:{token[-16:]}"
    if not await redis.get(key):
        raise HTTPException(status_code=401, detail="Refresh token revogado")

    repo = UserRepositoryImpl(db)
    user = await repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    from src.infrastructure.config.auth import create_refresh_token

    new_access = create_access_token(data={"sub": username})
    new_refresh = create_refresh_token(data={"sub": username})

    await redis.delete(key)
    ttl = REFRESH_TOKEN_EXPIRE_DAYS * 86400
    await redis.set(f"refresh:{username}:{new_refresh[-16:]}", "valid", ex=ttl)

    return Token(access_token=new_access, refresh_token=new_refresh)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token: str = Body(..., embed=True),
    redis: Redis = Depends(get_redis),
):
    username = decode_refresh_token(token)
    if username:
        await redis.delete(f"refresh:{username}:{token[-16:]}")
