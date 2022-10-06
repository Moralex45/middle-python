import abc
import datetime
import uuid

from src.db.models.permissions import PT, RPT
from src.db.models.roles import RT, URT
from src.db.models.users import AHT, UDT, UT
from src.db.models.social_account import SAT


class IAuthHistoryService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_user_name_and_user_agent(cls, user_name: str, user_agent: str) -> AHT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_user_name(cls, user_name: str) -> [AHT]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def stop_by_id(cls, _id: uuid.UUID):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def refresh_by_user_id_and_user_agent(cls, user_id: uuid.UUID, user_agent: str) -> AHT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, user_id: uuid.UUID, user_agent: str, ip: str) -> AHT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> AHT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_id(cls, _id: uuid.UUID):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete_by_user_id(cls, user_id: uuid.UUID):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_user_id_and_user_agent(cls, user_id: uuid.UUID, user_agent: str) -> AHT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_user_id(cls, user_id: uuid.UUID) -> [AHT]:
        raise NotImplementedError


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
    def update(cls, user_id: uuid.UUID,
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
    def get_filtered_by_user_id(cls, user_id: str) -> [PT]:
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


class ISocialAccountService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, _id: uuid.UUID) -> SAT | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(
        cls,
        user_id: uuid.UUID,
        social_id: str,
        social_name: str
    ) -> SAT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_filtered_by_user_id_and_social_id_and_social_name(
        cls,
        user_id: uuid.UUID,
        social_id: str,
        social_name: str
    ) -> SAT | None:
        raise NotImplementedError
