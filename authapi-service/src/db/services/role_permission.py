import uuid

from db.core import db_session
from db.models.permissions import RolePermissions
from db.services.base import IRolePermissionsService


class RolePermissionsService(IRolePermissionsService):
    def get_by_id(self, _id: uuid.UUID) -> RolePermissions:
        with db_session() as session:
            return session.query(RolePermissions).filter_by(id=_id).first()

    def delete_by_id(self, _id: uuid.UUID) -> None:
        pass

    def create(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> RolePermissions:
        pass

    def get_filtered(self, role_id: uuid.UUID) -> list[RolePermissions]:
        with db_session() as session:
            return session.query(RolePermissions).filter_by(role_id=role_id).all()
