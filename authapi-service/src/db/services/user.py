import datetime
import uuid
from typing import Optional

from sqlalchemy.exc import IntegrityError

from src.db.core import db_session
from src.db.models.users import User
from src.db.services.base import IUserService


class UserService(IUserService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> User | None:
        with db_session() as session:
            return session.query(User).filter_by(id=_id).first()

    @classmethod
    def get_by_username(cls, username: str) -> User | None:
        with db_session() as session:
            return session.query(User).filter_by(username=username).first()

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        """
        Raises:
            ValueError: On inability to fetch user with passed uuid

        """
        with db_session() as session:
            db_user = cls.get_by_id(_id)
            if db_user is not None:
                db_user.terminate_date = datetime.datetime.now()
                session.add(db_user)
                session.commit()
            else:
                raise ValueError(f'Unable to fetch user wih passed uuid {_id}')

    @classmethod
    def create(cls, username: str, password: str) -> User:
        """

        Raises:
            ValueError: When user already exist

        """
        with db_session() as session:
            db_user = User(username=username)
            db_user.password = password
            session.add_all([db_user])

            try:
                session.commit()

            except IntegrityError:
                raise ValueError('Unable to create user with passed parameters. '
                                 'Instance already exists')

            return cls.get_by_id(db_user.id)

    @classmethod
    def update(cls, _id: uuid.UUID, username: str | None = None, password: str | None = None) -> User:
        """
        Raises:
            ValueError: On inability to fetch user with passed uuid

        """
        with db_session() as session:
            db_user: User = session.query(User).filter_by(id=_id).first()
            if db_user is None:
                raise ValueError(f'Unable to fetch user wih passed uuid {_id}')
            if username is not None:
                db_user.username = username
            if password is not None:
                db_user.password = password
            session.commit()

            return cls.get_by_id(db_user.id)
