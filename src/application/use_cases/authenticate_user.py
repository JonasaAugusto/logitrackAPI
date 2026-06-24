from src.core.exceptions.user_exceptions import InvalidCredentialsError
from src.core.repositories.user_repository import IUserRepository
from src.infrastructure.config.auth import Token, create_access_token, create_refresh_token, verify_password


class AuthenticateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, username: str, password: str) -> Token:
        user = await self.repository.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
