from src.core.in_models.base import Base


class User(Base):
    password: str


class UserRegister(User):
    user_name: str


class UserLogin(UserRegister):
    remember: bool
