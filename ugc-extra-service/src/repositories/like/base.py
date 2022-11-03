from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

from src.models.inner.events.like import Like


class LikeRepositoryProtocol(ABC):
    @abstractmethod
    def get_movie_likes(self, movie_id: uuid.UUID) -> list[Like]:
        raise NotImplementedError

    @abstractmethod
    def get_user_likes(self, user_id: uuid.UUID) -> list[Like]:
        raise NotImplementedError

    @abstractmethod
    def create_like(self, like: Like) -> Like:
        raise NotImplementedError

    @abstractmethod
    def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID):
        raise NotImplementedError
