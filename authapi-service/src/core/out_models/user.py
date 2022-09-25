from typing import Any

from src.core.out_models.base import Base


class UserLoginHistory(Base):
    ip: str
    user_agent: str
    date_start: int
    date_end: int | None

    @classmethod
    def from_orm(cls, obj: Any):
        date_end = obj.date_end.timestamp() if obj.date_end is not None else None

        return cls(ip=obj.ip, user_agent=obj.user_agent, date_start=obj.date_start.timestamp(), date_end=date_end)
