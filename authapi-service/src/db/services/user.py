import uuid

from db.core import db_session
from db.models.users import User
from db.services.base import IUserService


class UserService(IUserService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> User:
        with db_session() as session:
            return session.query(User).filter_by(id=_id).first()
