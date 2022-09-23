from typing import Type

import redis

from src.cache.base import CacheService


class RedisCacheService(CacheService):
    def __init__(self, redis_instance: redis.Redis):
        self.redis: redis.Redis = redis_instance

    def get(self, key: str) -> str | None:
        data = self.redis.get(key).decode()
        if not data:
            return None

        return data

    def set(self, key: str, value: str, expire: int):
        self.redis.setex(key, expire, value)
