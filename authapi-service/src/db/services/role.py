from typing import List
import uuid

from sqlalchemy.exc import IntegrityError

from src.db.core import db_session
from src.db.models.roles import RT, Role
from src.db.services.base import IRoleService


class RoleService(IRoleService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> RT:
        with db_session() as session:
            return session.query(Role).filter_by(id=_id).first()

    @classmethod
    def get_all(cls) -> List[RT]:
        with db_session() as session:
            return session.query(Role).all()

    @classmethod
    def get_by_code(cls, code: int) -> RT:
        with db_session() as session:
            return session.query(Role).filter_by(code=code).first()

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        with db_session() as session:
            role = cls.get_by_id(_id)
            if role is not None:
                session.delete(role)
                session.commit()
            else:
                raise ValueError(f'Unable to fetch role wih passed uuid {_id}')

    @classmethod
    def create(cls, code: int, description: str) -> RT:
        with db_session() as session:
            db_role = Role(
                code=code,
                description=description
            )
            session.add_all([db_role])

            try:
                session.commit()
            except IntegrityError:
                raise ValueError(
                    'Unable to create role with passed code. '
                    'Instance already exists'
                )

            return cls.get_by_id(db_role.id)

    @classmethod
    def update(cls, _id: uuid.UUID, code: int, description: str) -> RT:
        with db_session() as session:
            role = cls.get_by_id(_id)
            if role is not None:
                role.code = code
                role.description = description
                session.add(role)
                session.commit()

                return cls.get_by_id(role.id)

            else:
                raise ValueError(f'Unable to fetch role wih passed uuid {_id}')
