from __future__ import annotations

import functools

import fastapi

from src.repositories.bookmark.mongodb import AsyncMongoDBBookmarkRepository
from src.services.storage import get_mongodb_instance


@functools.lru_cache()
def get_bookmark_repository(
        mongodb_instance=fastapi.Depends(get_mongodb_instance),
) -> AsyncMongoDBBookmarkRepository:
    return AsyncMongoDBBookmarkRepository(mongodb_instance)
