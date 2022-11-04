from __future__ import annotations

import uuid

from motor import motor_asyncio

import src.core.config as project_config
import src.core.exceptions.repositories as repositories_exception
from src.models.inner.events.bookmark import Bookmark
from src.repositories.bookmark.base import AsyncBookmarkRepositoryProtocol


class AsyncMongoDBBookmarkRepository(AsyncBookmarkRepositoryProtocol):
    def __init__(self, mongodb_instance: motor_asyncio.AsyncIOMotorClient):
        database = mongodb_instance[
            project_config.get_settings().mongodb_settings.mongodb_database
        ]
        self.collection: motor_asyncio.AsyncIOMotorCollection = database[
            project_config.get_settings().mongodb_settings.mongodb_bookmark_collection
        ]

    async def get_user_bookmarks(self, user_id: uuid.UUID) -> list[Bookmark]:
        query = {'user_id': str(user_id)}
        documents = await self.collection.find(query).to_list(await self.__count_documents(query))
        return [Bookmark(**document) for document in documents]

    async def create_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID, _id: uuid.UUID = None) -> Bookmark:
        """
        Raises:
            repositories_exception.DataAlreadyExistsError: on inability to create like

        """
        bookmark = Bookmark(
            _id=uuid.uuid4() if _id is None else _id,
            user_id=user_id,
            movie_id=movie_id,
        )
        if await self.get_bookmark(bookmark.user_id, bookmark.movie_id) is not None:
            raise repositories_exception.DataAlreadyExistsError()
        await self.collection.insert_one(bookmark.to_dict())
        return bookmark

    async def delete_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> None:
        """
        Raises:
            repositories_exception.DataDoesNotExistError: on inability to delete like

        """
        if await self.get_bookmark(user_id, movie_id) is None:
            raise repositories_exception.DataDoesNotExistError()
        query = {'user_id': str(user_id), 'movie_id': str(movie_id)}
        await self.collection.delete_one(query)

    async def get_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> Bookmark | None:
        query = {'user_id': str(user_id), 'movie_id': str(movie_id)}
        document: dict | None = await self.collection.find_one(query)  # type:ignore
        if document is not None:
            return Bookmark(**document)

        return None

    async def __count_documents(self, query: dict) -> int:
        return await self.collection.count_documents(query)
