from abc import ABC, abstractmethod
from typing import Any


class CacheService(ABC):
    @abstractmethod
    def get(self, key: str) -> Any | None:
        raise NotImplementedError()

    @abstractmethod
    def set(self, key: str, value: str, expire: int):
        raise NotImplementedError()
