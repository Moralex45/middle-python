import uuid

from core.in_models.base import Base


class UserRole(Base):
    user_id: uuid.UUID
    role_id: uuid.UUID
