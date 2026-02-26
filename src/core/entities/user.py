from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    """
    Entidade de Domínio: Usuário.
    Representa o usuário dentro das regras de negócio do sistema.
    """
    # Configuração para permitir conversão direta de objetos ORM (SQLAlchemy) para Pydantic
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None, description="ID único do usuário")
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário único")
    email: EmailStr = Field(..., description="Endereço de email válido")
    password_hash: str = Field(..., description="Hash da senha (nunca a senha em texto plano)")
    is_active: bool = Field(default=True, description="Indica se o usuário pode acessar o sistema")
    created_at: datetime = Field(default_factory=datetime.now, description="Data de criação do registro")