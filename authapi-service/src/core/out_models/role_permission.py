from typing import Type, TypeAlias
from uuid import UUID

from core.out_models.base import Base


class RolePermission(Base):
    id: UUID
    role_id: UUID
    perm_id: UUID

    @classmethod
    def from_pg(cls, **kwargs):
        return cls(id=kwargs['id'], role_id=kwargs['role_id'], permission_id=kwargs['perm_id'])
