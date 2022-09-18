import abc
import uuid

from db.models.permissions import RPT, PT
from db.models.roles import RT, URT


class IRolePermissionService(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, _id: uuid.UUID) -> RPT:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_by_id(self, _id: uuid.UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> RPT:
        raise NotImplementedError

    @abc.abstractmethod
    def get_filtered(self, role_id: uuid.UUID) -> list[RPT]:
        raise NotImplementedError


class IPermissionService(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, _id: uuid.UUID) -> PT:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> [PT]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_by_id(self, _id: uuid.UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, code: int) -> PT:
        raise NotImplementedError

    @abc.abstractmethod
    def recreate(self, _id: uuid.UUID, code: int) -> PT:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, _id: uuid.UUID, code: int) -> PT:
        raise NotImplementedError


class IRoleService(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, _id: uuid.UUID) -> RT:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> [RT]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_by_id(self, _id: uuid.UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, code: int, description: int) -> RT:
        raise NotImplementedError

    @abc.abstractmethod
    def recreate(self, _id: uuid.UUID, code: int, description: str) -> RT:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, _id: uuid.UUID, code: int, description: str) -> RT:
        raise NotImplementedError
