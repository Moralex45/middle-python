import uuid

from db.models.permissions import RolePermissions
from db.services.base import IRolePermissionsService
from db.core import db_session


class RolePermissionsService(IRolePermissionsService):
    def get_by_id(self, _id: uuid) -> RolePermissions:
        with db_session() as session:
            return session.query(RolePermissions).filter_by(id=_id).first()

    def delete_by_id(self, _id: uuid) -> None:
        pass

    def create(self, role_id: uuid, permission_id: uuid) -> RolePermissions:
        pass

    def get_filtered(self, role_id: uuid) -> list[RolePermissions]:
        with db_session() as session:
            return session.query(RolePermissions).filter_by(role_id=role_id).all()


