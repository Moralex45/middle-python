import uuid

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, VARCHAR, ForeignKey, TEXT
from models.base import BaseModel


class Role(BaseModel):
    __tablename__ = 'roles'

    code = Column(VARCHAR(255), nullable=False, unique=True)
    description = Column(TEXT(), default='')

    def __repr__(self):
        return f'({self.code}) {self.description}'


class UserRole(BaseModel):
    __tablename__ = 'users_roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, default=uuid.uuid4)
