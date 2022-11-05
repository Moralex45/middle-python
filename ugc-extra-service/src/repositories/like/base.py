from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from src.models.inner.events.like import UserToFilmLike


class AsyncLikeRepositoryProtocol(ABC):
    @abstractmethod
    async def get_movie_likes_amount(self, movie_id: uuid.UUID) -> int:
        raise NotImplementedError

    async def get_average_movie_mark(self, movie_id: uuid.UUID) -> float | None:
        raise NotImplementedError

    @abstractmethod
    async def create_like(
            self, user_id: uuid.UUID, movie_id: uuid.UUID, mark: int, _id: uuid.UUID = None,
    ) -> UserToFilmLike:
        raise NotImplementedError

    @abstractmethod
    async def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> UserToFilmLike | None:
        raise NotImplementedError
