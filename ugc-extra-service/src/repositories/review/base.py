from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from src.models.inner.events.review import Review


class ReviewRepositoryProtocol(ABC):
    @abstractmethod
    async def create_review(
            self, user_id: uuid.UUID, movie_id: uuid.UUID, review_text: str, _id: uuid.UUID | None = None,
    ) -> Review:
        raise NotImplementedError

    @abstractmethod
    async def get_review_by_user_id_and_movie_id(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> Review | None:
        raise NotImplementedError

    @abstractmethod
    async def get_review(self, review_id: uuid.UUID) -> Review | None:
        raise NotImplementedError

    @abstractmethod
    async def get_reviews_by_user_id(self, user_id: uuid.UUID) -> list[Review]:
        raise NotImplementedError

    @abstractmethod
    async def get_reviews_by_movie_id(self, movie_id: uuid.UUID) -> list[Review]:
        raise NotImplementedError
