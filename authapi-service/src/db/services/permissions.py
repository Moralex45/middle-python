import uuid

from db.core import db_session
from db.models.permissions import PT
from db.services.base import IPermissionService


class PermissionService(IPermissionService):
    def get_by_id(self, _id: uuid.UUID) -> PT:
        pass

    def get_all(self) -> [PT]:
        pass

    def delete_by_id(self, _id: uuid.UUID) -> None:
        pass

    def create(self, code: int) -> PT:
        pass

    def recreate(self, _id: uuid.UUID, code: int) -> PT:
        pass

    def update(self, _id: uuid.UUID, code: int) -> PT:
        pass