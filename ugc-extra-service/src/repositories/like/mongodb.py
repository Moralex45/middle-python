from __future__ import annotations
import uuid

from src.models.inner.events.like import Like
from src.repositories.like.base import LikeRepositoryProtocol


class MongoDBLikeRepository(LikeRepositoryProtocol):
    def get_movie_likes(self, movie_id: uuid.UUID) -> list[Like]:
        pass

    def get_user_likes(self, user_id: uuid.UUID) -> list[Like]:
        pass

    def create_like(self, like: Like) -> Like:
        pass

    def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID):
        pass
