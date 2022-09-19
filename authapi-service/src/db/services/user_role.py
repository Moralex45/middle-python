import uuid

from sqlalchemy.exc import IntegrityError

from src.db.core import db_session
from src.db.models.roles import UserRole
from src.db.services.base import IUserRoleService
from src.db.services.role import RoleService
from src.db.services.user import UserService


class UserRoleService(IUserRoleService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> UserRole:
        with db_session() as session:
            return session.query(UserRole).filter_by(id=_id).first()

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        """
        Raises:
            ValueError: On inability to fetch role permission with passed uuid

        """
        with db_session() as session:
            user_role = cls.get_by_id(_id)
            if user_role is not None:
                session.delete(user_role)
                session.commit()
            else:
                raise ValueError(f'Unable to fetch role permission wih passed uuid {_id}')

    @classmethod
    def create(cls, user_id: uuid.UUID, role_id: uuid.UUID) -> UserRole:
        """

        Raises:
            ValueError: When role or permission do not exist in db
            ValueError: When role_permission already exist with passed role and permission

        """
        with db_session() as session:
            db_user = UserService.get_by_id(user_id)
            db_role = RoleService.get_by_id(role_id)

            if db_role is None or db_user is None:
                raise ValueError(f'Unable to find role {role_id} or {user_id} instance with passed uuids')

            db_user_role = UserRole(role_id=role_id, user_id=user_id)
            session.add_all([db_user_role])

            try:
                session.commit()

            except IntegrityError:
                raise ValueError('Unable to create role_permission with passed role and permission. '
                                 'Instance already exists')

            return UserRoleService.get_by_id(db_user_role.id)

    @classmethod
    def get_filtered(cls, user_id: uuid.UUID) -> list[UserRole]:
        with db_session() as session:
            return session.query(UserRole).filter_by(user_id=user_id).all()
