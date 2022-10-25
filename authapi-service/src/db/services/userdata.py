import datetime
import uuid

from src.db.core import db_session
from src.db.models.users import UserData
from src.db.services.base import IUserDataService
from src.db.services.user import UserService


class UserDataService(IUserDataService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> UserData | None:
        with db_session() as session:
            return session.query(UserData).filter_by(id=_id).first()

    @classmethod
    def get_by_user_id(cls, user_id: uuid.UUID) -> UserData | None:
        with db_session() as session:
            return session.query(UserData).filter_by(user_id=user_id).first()

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        """
        Raises:
            ValueError: On inability to fetch userdata with passed uuid

        """
        with db_session() as session:
            db_user_data = cls.get_by_id(_id)
            if db_user_data is not None:
                session.delete(db_user_data)
                session.commit()
            else:
                raise ValueError(f'Unable to fetch userdata wih passed uuid {_id}')

    @classmethod
    def create(cls,
               user_id: uuid.UUID,
               first_name: str | None = None,
               last_name: str | None = None,
               email: str | None = None,
               birth_date: datetime.datetime | None = None) -> UserData:
        """

        Raises:
            ValueError: When user with passed user_id does not exist
            ValueError: When userdata already exist with passed user_id

        """
        with db_session() as session:
            db_user = UserService.get_by_id(user_id)
            if db_user is None:
                raise ValueError(f'Unable to fetch userdata wih passed uuid {user_id}')

            db_user_data = cls.get_by_user_id(user_id)
            if db_user_data is not None:
                raise ValueError(f'Unable to create userdata wih passed uuid {user_id}. '
                                 f'UserData already exist')

            db_userdata = UserData(user_id=user_id)
            if first_name is not None:
                db_userdata.first_name = first_name
            if last_name is not None:
                db_userdata.last_name = last_name
            if email is not None:
                db_userdata.email = email
            if birth_date is not None:
                db_userdata.birth_date = birth_date
            session.add_all([db_userdata])
            session.commit()

            return cls.get_by_id(db_userdata.id)

    @classmethod
    def update(cls, user_id: uuid.UUID,
               first_name: str | None = None,
               last_name: str | None = None,
               email: str | None = None,
               birth_date: datetime.datetime | None = None) -> UserData:
        """
        Raises:
            ValueError: On inability to fetch userdata with passed uuid

        """
        with db_session() as session:
            db_user_data = cls.get_by_user_id(user_id)
            if db_user_data is None:
                raise ValueError(f'Unable to fetch userdata wih passed uuid {user_id}')
            if first_name is not None:
                db_user_data.first_name = first_name
            if last_name is not None:
                db_user_data.last_name = last_name
            if email is not None:
                db_user_data.email = email
            if birth_date is not None:
                db_user_data.birth_date = birth_date
            session.add(db_user_data)
            session.commit()

            return cls.get_by_id(db_user_data.id)
