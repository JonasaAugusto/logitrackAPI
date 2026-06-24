from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.entities.user import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[UserEntity]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserEntity]: ...

    @abstractmethod
    async def list(self, skip: int, limit: int) -> List[UserEntity]: ...

    @abstractmethod
    async def create(self, entity: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def update(self, entity: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def delete(self, user_id: int) -> None: ...
