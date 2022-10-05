from src.core.out_models.base import Base


class SuccessfulLogin(Base):
    access_token: str
    access_token_expire_timestamp: float
    refresh_token: str
    refresh_token_expire_timestamp: float
