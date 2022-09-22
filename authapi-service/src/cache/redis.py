from typing import Type

import redis

from cache.base import CacheService


class RedisCacheService(CacheService):
    def __init__(self, redis_instance: redis.Redis):
        self.redis: redis.Redis = redis_instance

    def get(self, key: str) -> bytes | None:
        data = self.redis.get(key)
        if not data:
            return None

        return data

    def set(self, key: str, value: str, expire: int):
        self.redis.setex(key, expire, value)
