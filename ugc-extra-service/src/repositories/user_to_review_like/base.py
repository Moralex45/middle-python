from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from src.models.inner.events.user_to_review_like import UserToReviewLike


class AsyncUserToReviewLikeRepositoryProtocol(ABC):
    @abstractmethod
    async def create_like(
            self, user_id: uuid.UUID, review_id: uuid.UUID, mark: int, _id: uuid.UUID | None = None,
    ) -> UserToReviewLike:
        raise NotImplementedError

    @abstractmethod
    async def delete_like(self, user_id: uuid.UUID, review_id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_like(self, user_id: uuid.UUID, review_id: uuid.UUID) -> UserToReviewLike | None:
        raise NotImplementedError
