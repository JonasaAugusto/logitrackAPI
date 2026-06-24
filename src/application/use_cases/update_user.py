from src.application.dtos.user_dto import UserUpdateDTO
from src.core.entities.user import UserEntity
from src.core.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundError
from src.core.repositories.user_repository import IUserRepository
from src.infrastructure.config.auth import hash_password


class UpdateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, user_id: int, dto: UserUpdateDTO) -> UserEntity:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        update_data = dto.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"] != user.email:
            if await self.repository.get_by_email(update_data["email"]):
                raise UserAlreadyExistsError("Email", update_data["email"])
            user.email = update_data["email"]

        if "username" in update_data and update_data["username"] != user.username:
            if await self.repository.get_by_username(update_data["username"]):
                raise UserAlreadyExistsError("Username", update_data["username"])
            user.username = update_data["username"]

        if "password" in update_data:
            user.password_hash = hash_password(update_data["password"])

        if "is_active" in update_data:
            user.is_active = update_data["is_active"]

        return await self.repository.update(user)
