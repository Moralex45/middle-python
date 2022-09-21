from src.core.out_models.base import Base


class SuccessfulLogin(Base):
    access_token: str
    refresh_token: str
