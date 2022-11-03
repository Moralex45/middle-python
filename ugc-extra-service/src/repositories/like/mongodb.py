from __future__ import annotations
import uuid

from motor import motor_asyncio

from src.models.inner.events.like import Like
from src.repositories.like.base import AsyncLikeRepositoryProtocol
import src.core.config as project_config


class AsyncMongoDBLikeRepository(AsyncLikeRepositoryProtocol):
    def __init__(self, mongodb_instance: motor_asyncio.AsyncIOMotorClient):
        database = mongodb_instance[project_config.get_settings().mongodb_settings.mongodb_database]
        self.collection = database[project_config.get_settings().mongodb_settings.mongodb_likes_collection]

    async def get_movie_likes(self, movie_id: uuid.UUID) -> list[Like]:
        pass

    async def get_user_likes(self, user_id: uuid.UUID) -> list[Like]:
        pass

    async def create_like(self, like: Like) -> Like:
        pass

    async def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID):
        pass
