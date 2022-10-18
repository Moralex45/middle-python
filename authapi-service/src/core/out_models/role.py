import uuid
from typing import Any

from src.core.out_models.base import Base


class Role(Base):
    id: uuid.UUID # noqa
    code: int
    description: str

    @classmethod
    def from_orm(cls, obj: Any):
        return cls(id=obj.id, code=obj.code, description=obj.description)
