from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from src.models.inner.events.bookmark import Bookmark


class AsyncBookmarkRepositoryProtocol(ABC):
    @abstractmethod
    async def get_user_bookmarks(self, user_id: uuid.UUID) -> list[Bookmark]:
        raise NotImplementedError

    @abstractmethod
    async def create_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID, _id: uuid.UUID | None = None) -> Bookmark:
        raise NotImplementedError

    @abstractmethod
    async def delete_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> Bookmark | None:
        raise NotImplementedError
