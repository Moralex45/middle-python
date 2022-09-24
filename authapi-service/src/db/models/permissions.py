from typing import TypeVar

from sqlalchemy import INT, Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from src.db.models.base import BaseModel
from src.db.models.roles import Role

PT = TypeVar('PT')
RPT = TypeVar('RPT')


class Permission(BaseModel):
    __tablename__ = 'permissions'
    __table_args__ = ({'extend_existing': True},)

    code = Column(INT(), nullable=False, unique=True)

    def __repr__(self):
        return f'({self.code}) {self.description}'


class RolePermissions(BaseModel):
    __tablename__ = 'roles_permissions'
    __table_args__ = (UniqueConstraint('role_id', 'perm_id'),
                      {'extend_existing': True})

    role_id = Column(UUID(as_uuid=True), ForeignKey(Role.id, ondelete='CASCADE'), nullable=False)
    perm_id = Column(UUID(as_uuid=True), ForeignKey(Permission.id, ondelete='CASCADE'), nullable=False)
