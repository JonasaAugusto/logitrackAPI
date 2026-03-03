import pytest

from src.application.dtos.user_dto import UserCreateDTO


def test_user_create_dto_valid():
    dto = UserCreateDTO(username="Jonas Silva", email="jonas@example.com", password="12345678")
    assert dto.email == "jonas@example.com"


def test_user_create_dto_short_password_fails():
    with pytest.raises(ValueError):
        UserCreateDTO(username="Jonas", email="jonas@email.com", password="123")
