import uuid

from sqlalchemy import TEXT, VARCHAR, Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from db.models.base import BaseModel
from db.models.users import User


class Role(BaseModel):
    __tablename__ = 'roles'
    __table_args__ = ({'extend_existing': True},)

    code = Column(VARCHAR(255), nullable=False, unique=True)
    description = Column(TEXT(), default='')

    def __repr__(self):
        return f'({self.code}) {self.description}'


class UserRole(BaseModel):
    __tablename__ = 'users_roles'
    __table_args__ = (UniqueConstraint('user_id', 'role_id'),
                      {'extend_existing': True})

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE'), nullable=False, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey(Role.id, ondelete='CASCADE'), nullable=False, default=uuid.uuid4)
