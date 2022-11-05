from __future__ import annotations

import functools

import fastapi

from src.repositories.review.mongodb import AsyncMongoDBReviewRepository
from src.services.storage import get_mongodb_instance


@functools.lru_cache()
def get_review_repository(
        mongodb_instance=fastapi.Depends(get_mongodb_instance),
) -> AsyncMongoDBReviewRepository:
    return AsyncMongoDBReviewRepository(mongodb_instance)
