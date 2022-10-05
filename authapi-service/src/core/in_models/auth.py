from typing import Optional

from src.core.in_models.base import Base


class RefreshSession(Base):
    access_token: str
    refresh_token: str
    user_agent: str


class Logout(Base):
    all_devices: Optional[bool]
