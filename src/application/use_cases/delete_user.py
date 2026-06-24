from src.core.exceptions.user_exceptions import UnauthorizedError, UserNotFoundError
from src.core.repositories.user_repository import IUserRepository


class DeleteUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, user_id: int, current_username: str) -> dict:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        if user.username != current_username:
            raise UnauthorizedError()

        await self.repository.delete(user_id)
        return {"message": "Usuário deletado com sucesso", "deleted_id": user_id, "deleted_username": user.username}
