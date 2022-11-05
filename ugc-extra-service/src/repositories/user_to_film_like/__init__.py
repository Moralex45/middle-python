from __future__ import annotations

import functools

import fastapi

from src.repositories.user_to_film_like.mongodb import AsyncMongoDBUserToFilmLikeRepository
from src.services.storage import get_mongodb_instance


@functools.lru_cache()
def get_user_to_film_like_repository(
        mongodb_instance=fastapi.Depends(get_mongodb_instance),
) -> AsyncMongoDBUserToFilmLikeRepository:
    return AsyncMongoDBUserToFilmLikeRepository(mongodb_instance)
