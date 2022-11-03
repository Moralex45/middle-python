from __future__ import annotations
import functools

import fastapi

from src.repositories.like.mongodb import AsyncMongoDBLikeRepository
from src.services.storage import get_mongodb_instance


@functools.lru_cache()
def get_like_repository(
        mongodb_instance=fastapi.Depends(get_mongodb_instance),
) -> AsyncMongoDBLikeRepository:
    return AsyncMongoDBLikeRepository(mongodb_instance)
