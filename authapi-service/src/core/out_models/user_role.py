import uuid
from typing import Any

from src.core.out_models.base import Base


class UserRole(Base):
    id: uuid.UUID # noqa
    user_id: uuid.UUID
    role_id: uuid.UUID

    @classmethod
    def from_orm(cls, obj: Any):
        return cls(id=obj.id, role_id=obj.role_id, user_id=obj.user_id)
