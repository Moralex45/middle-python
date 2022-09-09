from abc import ABC, abstractmethod
from typing import Any, Type
from models import T


class AsyncStorage(ABC):
    @abstractmethod
    async def get_by_id(self, _id: str, base_class: Type[T], **kwargs) -> T | None:
        raise NotImplementedError()

    @abstractmethod
    async def search(self, body: Any, base_class: Type[T], **kwargs) -> list[T] | None:
        raise NotImplementedError()


class AsyncStorageService(AsyncStorage):
    @abstractmethod
    async def close(self):
        raise NotImplementedError()
