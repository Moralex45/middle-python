from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

from src.models.inner.events.like import Like


class AsyncLikeRepositoryProtocol(ABC):
    @abstractmethod
    async def get_movie_likes_amount(self, movie_id: uuid.UUID) -> int:
        raise NotImplementedError

    async def get_average_movie_mark(self, movie_id: uuid.UUID) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def create_like(self,  user_id: uuid.UUID, movie_id: uuid.UUID, mark: int, device_fingerprint: str) -> Like:
        raise NotImplementedError

    @abstractmethod
    async def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> None:
        raise NotImplementedError
