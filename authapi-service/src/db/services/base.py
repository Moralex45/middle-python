import abc
import datetime
import uuid

from src.db.models.permissions import PT, RPT
from src.db.models.roles import RT, URT
from src.db.models.users import UDT, UT


class IRolePermissionService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> RPT | None:
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
    def get_by_id(cls, _id: uuid.UUID) -> URT | None:
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
    def get_by_id(cls, _id: uuid.UUID) -> UT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_username(cls, username: str) -> UT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: uuid.UUID) -> UT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, username: str, password: str) -> UT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update(cls, _id: uuid.UUID, username: str, password: str) -> UT:
        pass


class IUserDataService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> UDT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_user_id(cls, user_id: uuid.UUID) -> UDT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: uuid.UUID) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls,
               user_id: uuid.UUID,
               first_name: str | None = None,
               last_name: str | None = None,
               email: str | None = None,
               birth_date: datetime.datetime | None = None) -> UDT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update(cls, _id: uuid.UUID,
               first_name: str | None = None,
               last_name: str | None = None,
               email: str | None = None,
               birth_date: datetime.datetime | None = None) -> UDT:
        raise NotImplementedError


class IPermissionService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> PT | None:
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
    def update(cls, _id: uuid.UUID, code: int) -> PT:
        raise NotImplementedError


class IRoleService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> RT | None:
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
    def update(cls, _id: uuid.UUID, code: int, description: str) -> RT:
        raise NotImplementedError
