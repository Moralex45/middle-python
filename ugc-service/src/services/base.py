from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar('T')


class EventServiceInterface(ABC):
    @abstractmethod
    def produce_movie_watching(self, event: T) -> None:
        raise NotImplementedError
