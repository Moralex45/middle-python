import uuid

from db.core import db_session
from db.models.permissions import RolePermissions
from db.services.base import IRolePermissionService


class RolePermissionService(IRolePermissionService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> RolePermissions:
        with db_session() as session:
            return session.query(RolePermissions).filter_by(id=_id).first()

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        """
        Raises:
            ValueError: On inability to fetch role permission with passed uuid

        """
        with db_session() as session:
            role_permission = cls.get_by_id(_id)
            if role_permission is not None:
                session.delete(role_permission)
                session.commit()
            else:
                raise ValueError(f'Unable to fetch role permission wih passed uuid {_id}')

    @classmethod
    def create(cls, role_id: uuid.UUID, permission_id: uuid.UUID) -> RolePermissions:
        pass

    @classmethod
    def get_filtered(cls, role_id: uuid.UUID) -> list[RolePermissions]:
        with db_session() as session:
            return session.query(RolePermissions).filter_by(role_id=role_id).all()
