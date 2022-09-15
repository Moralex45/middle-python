from abc import ABC, abstractmethod
from typing import Any, Type

from models import T


class AsyncCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any | None:
        raise NotImplementedError()

    @abstractmethod
    async def set(self, key: str, value: str, expire: int):
        raise NotImplementedError()


class AsyncCacheService(AsyncCache):
    @abstractmethod
    async def get_single(self, key: str, base_class: Type[T]) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def set_single(self, key: str, data: T, expire: int):
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, key: str, base_class: Type[T]) -> list[T] | None:
        raise NotImplementedError()

    @abstractmethod
    async def set_list(self, key: str, data: list[T], expire: int):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()
