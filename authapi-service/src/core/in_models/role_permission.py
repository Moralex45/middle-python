import uuid

from src.core.in_models.base import Base


class RolePermission(Base):
    role_id: uuid.UUID
    permission_id: uuid.UUID
