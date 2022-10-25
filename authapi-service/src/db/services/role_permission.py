import uuid

from sqlalchemy.exc import IntegrityError

from src.db.core import db_session
from src.db.models.permissions import RolePermissions
from src.db.services.base import IRolePermissionService
from src.db.services.permissions import PermissionService
from src.db.services.role import RoleService


class RolePermissionService(IRolePermissionService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> RolePermissions | None:
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
        """

        Raises:
            ValueError: When role or permission do not exist in db
            ValueError: When role_permission already exist with passed role and permission

        """
        with db_session() as session:
            db_role = RoleService.get_by_id(role_id)
            db_permission = PermissionService.get_by_id(permission_id)

            if db_role is None or db_permission is None:
                raise ValueError(f'Unable to find role {role_id} or {permission_id} instance with passed uuids')

            db_role_permission = RolePermissions(role_id=role_id, perm_id=permission_id)
            session.add_all([db_role_permission])

            try:
                session.commit()

            except IntegrityError:
                raise ValueError('Unable to create role_permission with passed role and permission. '
                                 'Instance already exists')

            return RolePermissionService.get_by_id(db_role_permission.id)

    @classmethod
    def get_filtered(cls, role_id: uuid.UUID) -> list[RolePermissions]:
        with db_session() as session:
            return session.query(RolePermissions).filter_by(role_id=role_id).all()
