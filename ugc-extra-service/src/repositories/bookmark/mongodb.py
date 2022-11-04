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

    async def get_users_bookmark(self, user_id: uuid.UUID) -> list[Bookmark]:
        pass

    async def create_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> Bookmark:
        pass

    async def delete_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> None:
        pass
