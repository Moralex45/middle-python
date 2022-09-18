import abc
import uuid

from db.models.permissions import PT, RPT
from db.models.roles import RT, URT
from db.models.users import UT


class IRolePermissionService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> RPT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, role_id: uuid.UUID, permission_id: uuid.UUID) -> RPT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_filtered(cls, role_id: uuid.UUID) -> list[RPT]:
        raise NotImplementedError


class IUserRoleService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> URT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, user_id: uuid.UUID, role_id: uuid.UUID) -> URT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_filtered(cls, user_id: uuid.UUID) -> list[URT]:
        raise NotImplementedError


class IUserService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> UT:
        raise NotImplementedError


class IPermissionService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> PT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_all(cls) -> [PT]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, code: int) -> PT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def recreate(cls, _id: uuid.UUID, code: int) -> PT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update(cls, _id: uuid.UUID, code: int) -> PT:
        raise NotImplementedError


class IRoleService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> RT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_all(cls) -> [RT]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, code: int, description: int) -> RT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def recreate(cls, _id: uuid.UUID, code: int, description: str) -> RT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update(cls, _id: uuid.UUID, code: int, description: str) -> RT:
        raise NotImplementedError
