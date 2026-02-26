from fastapi import APIRouter, HTTPException, status

from application.dtos.user_dto import UserCreate, UserResponse
from core.entities.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate):
    """
    Cria um novo usuário.
    Utiliza UserCreate (DTO) para validação de entrada e
    UserResponse (DTO) para formatar a saída.
    """

    new_user = User(
        id=1,
        username=user_in.username,
        email=user_in.email,
        password_hash="hashed_secret",  # Simulação de hash
        is_active=True,
    )

    return new_user
