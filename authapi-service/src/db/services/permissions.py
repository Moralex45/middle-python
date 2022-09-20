import uuid

from src.db.core import db_session
from src.db.models.permissions import PT, Permission
from src.db.services.base import IPermissionService


class PermissionService(IPermissionService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> Permission | None:
        with db_session() as session:
            return session.query(Permission).filter_by(id=_id).first()

    @classmethod
    def get_all(cls) -> [PT]:
        pass

    @classmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        pass

    @classmethod
    def create(cls, code: int) -> PT:
        pass

    @classmethod
    def recreate(cls, _id: uuid.UUID, code: int) -> PT:
        pass

    @classmethod
    def update(cls, _id: uuid.UUID, code: int) -> PT:
        pass
