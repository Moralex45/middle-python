from src.models.base import Base


class User(Base):
    email: str
    first_name: str
    last_name: str
