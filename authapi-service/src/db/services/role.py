import uuid

from db.models.roles import RT
from db.services.base import IRoleService


class RoleService(IRoleService):
    def get_by_id(self, _id: uuid.UUID) -> RT:
        pass

    def get_all(self) -> [RT]:
        pass

    def delete_by_id(self, _id: uuid.UUID) -> None:
        pass

    def create(self, code: int, description: int) -> RT:
        pass

    def recreate(self, _id: uuid.UUID, code: int, description: str) -> RT:
        pass

    def update(self, _id: uuid.UUID, code: int, description: str) -> RT:
        pass

