from typing import List
import uuid

from sqlalchemy.exc import IntegrityError

from db.models.roles import UserRole, Role
from src.db.core import db_session
from src.db.models.permissions import PT, Permission, RolePermissions
from src.db.services.base import IPermissionService


class PermissionService(IPermissionService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> Permission | None:
        with db_session() as session:
            return session.query(Permission).filter_by(id=_id).first()

    @classmethod
    def get_by_code(cls, code: int) -> PT:
        with db_session() as session:
            return session.query(Permission).filter_by(code=code).first()

    @classmethod
    def get_all(cls) -> List[PT]:
        with db_session() as session:
            return session.query(Permission).all()

    @classmethod
    def get_filtered_by_user_id(cls, user_id: str) -> [Permission]:
        with db_session() as session:
            user_permissions = session.query(Permission) \
                .join(RolePermissions, Permission.id == RolePermissions.perm_id) \
                .join(UserRole, RolePermissions.role_id == UserRole.role_id) \
                .filter(UserRole.user_id == user_id) \
                .all()

            return user_permissions

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        with db_session() as session:
            permission = cls.get_by_id(_id)
            if permission is not None:
                session.delete(permission)
                session.commit()
            else:
                raise ValueError(f'Unable to fetch permission wih passed uuid {_id}')

    @classmethod
    def create(cls, code: int) -> PT:
        with db_session() as session:
            db_permission = Permission(
                code=code
            )

            session.add_all([db_permission])

            try:
                session.commit()
            except IntegrityError:
                raise ValueError(
                    'Unable to create permission with passed code. '
                    'Instance already exists'
                )

            return cls.get_by_id(db_permission.id)

    @classmethod
    def update(cls, _id: uuid.UUID, code: int) -> PT:
        with db_session() as session:
            permission = cls.get_by_id(_id)
            if permission is not None:
                permission.code = code

                session.add(permission)
                session.commit()

                return cls.get_by_id(permission.id)

            else:
                raise ValueError(f'Unable to fetch permission wih passed uuid {_id}')
