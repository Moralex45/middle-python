from uuid import UUID

from core.in_models.base import Base


class RolePermission(Base):
    role_id: UUID
    perm_id: UUID
