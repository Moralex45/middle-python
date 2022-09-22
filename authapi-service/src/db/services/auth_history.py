import uuid

from sqlalchemy.exc import IntegrityError

from db.core import db_session
from db.models.users import AuthHistory
from db.services.base import IAuthHistoryService


class AuthHistoryService(IAuthHistoryService):
    @classmethod
    def create(cls, user_id: uuid.UUID, user_agent: str, ip: str) -> AuthHistory:
        with db_session() as session:
            db_auth_history = AuthHistory(
                ip=ip,
                user_id=user_id,
                user_agent=user_agent
            )
            session.add(db_auth_history)

            try:
                session.commit()
            except IntegrityError:
                raise ValueError(
                    'Unable to create auth history with passed data. '
                    'Instance already exists'
                )

            return cls.get_by_id(db_auth_history.id)

    @classmethod
    def get_by_id(cls, _id: uuid.UUID):
        with db_session() as session:
            return session.query(AuthHistory).filter_by(id=_id).first()

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID):
        with db_session() as session:
            auth_history = cls.get_by_id(_id)
            if auth_history is not None:
                session.delete(auth_history)
                session.commit()
            else:
                raise ValueError(f'Unable to fetch auth history wih passed uuid {_id}')

    @classmethod
    def delete_by_user_id(cls, user_id: uuid.UUID):
        with db_session() as session:
            db_auth_histories = cls.get_by_user_id(user_id)
            for db_auth_history in db_auth_histories:
                session.delete(db_auth_history)

            session.commit()

    @classmethod
    def get_by_user_id_and_user_agent(cls, user_id: uuid.UUID, user_agent: str) -> AuthHistory | None:
        with db_session() as session:
            return session.query(AuthHistory).filter_by(user_id=user_id).filter_by(user_agent=user_agent).first()

    @classmethod
    def get_by_user_id(cls, user_id: uuid.UUID) -> [AuthHistory]:
        with db_session() as session:
            return session.query(AuthHistory).filter_by(user_id=user_id).all()
