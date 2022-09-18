import abc
from uuid import UUID

from db.models.permissions import RPT, PT
from db.models.roles import RT, URT


class IRolePermissionService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: UUID) -> RPT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: UUID) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, role_id: UUID, permission_id: UUID) -> RPT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_filtered(cls, role_id: UUID) -> list[RPT]:
        raise NotImplementedError


class IPermissionService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: UUID) -> PT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_all(cls) -> [PT]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: UUID) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, code: int) -> PT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def recreate(cls, _id: UUID, code: int) -> PT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update(cls, _id: UUID, code: int) -> PT:
        raise NotImplementedError


class IRoleService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: UUID) -> RT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_all(cls) -> [RT]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: UUID) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, code: int, description: int) -> RT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def recreate(cls, _id: UUID, code: int, description: str) -> RT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update(cls, _id: UUID, code: int, description: str) -> RT:
        raise NotImplementedError
