from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.user import UserEntity
from src.core.repositories.user_repository import IUserRepository
from src.infrastructure.persistence.models.user import User


def _to_entity(model: User) -> UserEntity:
    return UserEntity(
        id=model.id,  # type: ignore[arg-type]
        username=model.username,  # type: ignore[arg-type]
        email=model.email,  # type: ignore[arg-type]
        password_hash=model.password_hash,  # type: ignore[arg-type]
        is_active=model.is_active,  # type: ignore[arg-type]
        created_at=model.created_at,  # type: ignore[arg-type]
        updated_at=model.updated_at,  # type: ignore[arg-type]
    )


class UserRepositoryImpl(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        result = await self.db.execute(select(User).where(User.email == email))
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        result = await self.db.execute(select(User).where(User.username == username))
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list(self, skip: int, limit: int) -> List[UserEntity]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return [_to_entity(m) for m in result.scalars().all()]

    async def create(self, entity: UserEntity) -> UserEntity:
        model = User(
            username=entity.username,
            email=entity.email,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return _to_entity(model)

    async def update(self, entity: UserEntity) -> UserEntity:
        result = await self.db.execute(select(User).where(User.id == entity.id))
        model = result.scalar_one()
        model.username = entity.username  # type: ignore[assignment]
        model.email = entity.email  # type: ignore[assignment]
        model.password_hash = entity.password_hash  # type: ignore[assignment]
        model.is_active = entity.is_active  # type: ignore[assignment]
        await self.db.commit()
        await self.db.refresh(model)
        return _to_entity(model)

    async def delete(self, user_id: int) -> None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        model = result.scalar_one()
        await self.db.delete(model)
        await self.db.commit()
