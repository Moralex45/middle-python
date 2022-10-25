import uuid
from typing import Any

from src.core.out_models.base import Base


class Permission(Base):
    id: uuid.UUID  # noqa
    code: int

    @classmethod
    def from_orm(cls, obj: Any):
        return cls(id=obj.id, code=obj.code)
