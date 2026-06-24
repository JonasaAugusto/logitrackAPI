from src.application.dtos.user_dto import UserCreateDTO
from src.core.entities.user import UserEntity
from src.core.exceptions.user_exceptions import UserAlreadyExistsError
from src.core.repositories.user_repository import IUserRepository
from src.infrastructure.config.auth import hash_password


class CreateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, dto: UserCreateDTO) -> UserEntity:
        if await self.repository.get_by_email(dto.email):
            raise UserAlreadyExistsError("Email", dto.email)

        if await self.repository.get_by_username(dto.username):
            raise UserAlreadyExistsError("Username", dto.username)

        entity = UserEntity(
            username=dto.username,
            email=dto.email,
            password_hash=hash_password(dto.password),
        )
        return await self.repository.create(entity)
