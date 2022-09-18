import uuid

from db.core import db_session
from db.models.roles import RT, Role
from db.services.base import IRoleService


class RoleService(IRoleService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> RT:
        with db_session() as session:
            return session.query(Role).filter_by(id=_id).first()

    @classmethod
    def get_all(cls) -> [RT]:
        pass

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        pass

    @classmethod
    def create(cls, code: int, description: int) -> RT:
        pass

    @classmethod
    def recreate(cls, _id: uuid.UUID, code: int, description: str) -> RT:
        pass

    @classmethod
    def update(cls, _id: uuid.UUID, code: int, description: str) -> RT:
        pass

