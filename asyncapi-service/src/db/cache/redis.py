from typing import Type

import backoff
import orjson
from aioredis import Redis
from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder

from db.cache.base import AsyncCache, AsyncCacheService
from models import T


class AsyncRedisCache(AsyncCache):
    def __init__(self, redis_pool: Redis):
        self.redis: Redis = redis_pool

    @backoff.on_exception(backoff.expo, [ConnectionRefusedError], max_time=10)
    async def get(self, key: str) -> bytes | None:
        data = await self.redis.get(key)
        if not data:
            return None

        return data

    @backoff.on_exception(backoff.expo, [ConnectionRefusedError], max_time=10)
    async def set(self, key: str, value: str, expire: int):
        await self.redis.set(key, value, expire=expire)


class AsyncRedisCacheService(AsyncRedisCache, AsyncCacheService):
    def __init__(self, redis_pool: Redis):
        super().__init__(redis_pool)

    async def get_single(self, key: str, base_class: Type[T]) -> T | None:
        data = await self.redis.get(key)
        if not data:
            return None

        return base_class.parse_raw(data)

    async def set_single(self, key: str, data: T, expire: int):
        await self.redis.set(key, data.json(), expire=expire)

    async def get_list(self, key: str, base_class: Type[T]) -> list[T] | None:
        data = await self.redis.get(key)
        if not data:
            return None

        return parse_obj_as(list[base_class], orjson.loads(data))

    async def set_list(self, key: str, data: list[T], expire: int):
        await self.redis.set(key, orjson.dumps(data, default=pydantic_encoder).decode(), expire=expire)

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()
