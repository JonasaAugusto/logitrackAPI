class UserNotFoundError(Exception):
    def __init__(self, identifier: str | int):
        super().__init__(f"Usuário não encontrado: {identifier}")


class UserAlreadyExistsError(Exception):
    def __init__(self, field: str, value: str):
        super().__init__(f"{field} já registrado: {value}")


class InvalidCredentialsError(Exception):
    def __init__(self):
        super().__init__("Username ou senha incorretos")


class UnauthorizedError(Exception):
    def __init__(self):
        super().__init__("Não autorizado a realizar esta operação")
