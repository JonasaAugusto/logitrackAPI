from src.core.entities.user import UserEntity
from src.core.exceptions.user_exceptions import UserNotFoundError
from src.core.repositories.user_repository import IUserRepository


class GetUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> UserEntity:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user


class ListUsersUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, skip: int = 0, limit: int = 50) -> list[UserEntity]:
        return await self.repository.list(skip=skip, limit=limit)
