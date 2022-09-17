import abc
import uuid
from db.models.permissions import RPT


class IRolePermissionsService(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, _id: uuid) -> RPT:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_by_id(self, _id: uuid) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, role_id: uuid, permission_id: uuid) -> RPT:
        raise NotImplementedError

    @abc.abstractmethod
    def get_filtered(self, role_id: uuid) -> list[RPT]:
        raise NotImplementedError
