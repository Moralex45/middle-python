from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, VARCHAR, ForeignKey
from models.base import BaseModel


class Permission(BaseModel):
    __tablename__ = 'permissions'

    code = Column(VARCHAR(255), nullable=False, unique=True)

    def __repr__(self):
        return f'({self.code}) {self.description}'


class RolePermissions(BaseModel):
    __tablename__ = 'roles_permissions'

    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    perm_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False)
