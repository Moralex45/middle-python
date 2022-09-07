from abc import ABC, abstractmethod
from typing import Any, Type


class AsyncStorage(ABC):
    @abstractmethod
    async def get_by_id(self, _id: str, base_class: Type[Any]) -> Any | None:
        raise NotImplementedError()

    @abstractmethod
    async def search(self, body: Any, base_class: Type[Any]) -> list[Any] | None:
        raise NotImplementedError()


class AsyncStorageService(AsyncStorage):
    @abstractmethod
    async def close(self):
        raise NotImplementedError()
