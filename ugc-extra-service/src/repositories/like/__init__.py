import functools

from src.repositories.like.mongodb import MongoDBLikeRepository

like_repository: MongoDBLikeRepository | None = None


@functools.lru_cache()
def get_like_repository() -> MongoDBLikeRepository | None:
    return like_repository
