from uuid import UUID

from core.out_models.base import Base


class RolePermission(Base):
    id: UUID
    role_id: UUID
    perm_id: UUID
