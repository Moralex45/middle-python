from typing import Optional

from src.core.in_models.base import Base


class User(Base):
    password: str


class UserRegister(User):
    user_name: str


class UserLogin(UserRegister):
    remember: bool


class UserUpdate(User):
    new_password: Optional[str]
    user_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    birth_date: Optional[int]
