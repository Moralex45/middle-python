import uuid
from typing import Any

from src.core.out_models.base import Base


class RolePermission(Base):
    id: uuid.UUID  # noqa
    role_id: uuid.UUID
    permission_id: uuid.UUID

    @classmethod
    def from_orm(cls, obj: Any):
        return cls(id=obj.id, role_id=obj.role_id, permission_id=obj.perm_id)
