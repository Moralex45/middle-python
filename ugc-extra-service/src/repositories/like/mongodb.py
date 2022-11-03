from __future__ import annotations
import uuid

from motor import motor_asyncio

from src.models.inner.events.like import Like
from src.repositories.like.base import AsyncLikeRepositoryProtocol
import src.core.config as project_config


class AsyncMongoDBLikeRepository(AsyncLikeRepositoryProtocol):
    def __init__(self, mongodb_instance: motor_asyncio.AsyncIOMotorClient):
        database = mongodb_instance[
            project_config.get_settings().mongodb_settings.mongodb_database
        ]
        self.collection: motor_asyncio.AsyncIOMotorCollection = database[
            project_config.get_settings().mongodb_settings.mongodb_likes_collection
        ]

    async def get_movie_likes(self, movie_id: uuid.UUID) -> list[Like]:
        query = {'movie_id': str(movie_id)}
        documents = await self.collection.find(query).to_list(await self.__count_documents(query))
        return [Like(**document) for document in documents]

    async def get_user_likes(self, user_id: uuid.UUID) -> list[Like]:
        query = {'user_id': str(user_id)}
        documents = await self.collection.find(query).to_list(await self.__count_documents(query))
        return [Like(**document) for document in documents]

    async def create_like(self, like: Like) -> None:
        await self.collection.insert_one(like.to_dict())

    async def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> None:
        query = {'user_id': str(user_id), 'movie_id': str(movie_id)}
        await self.collection.delete_one(query)

    async def __count_documents(self, query: dict) -> int:
        return await self.collection.count_documents(query)
