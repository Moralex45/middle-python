from typing import TypeVar

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, VARCHAR, ForeignKey, UniqueConstraint
from db.models.base import BaseModel

PT = TypeVar('PT')
RPT = TypeVar('RPT')


class Permission(BaseModel):
    __tablename__ = 'permissions'
    # __table_args__ = ({'extend_existing': True},)

    code = Column(VARCHAR(255), nullable=False, unique=True)

    def __repr__(self):
        return f'({self.code}) {self.description}'


class RolePermissions(BaseModel):
    __tablename__ = 'roles_permissions'
    __table_args__ = (UniqueConstraint('role_id', 'perm_id'),
                      )

    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    perm_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False)
