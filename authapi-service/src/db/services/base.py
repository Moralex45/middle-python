import abc
import uuid

from db.models.permissions import RPT


class IRolePermissionsService(abc.ABC):
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
