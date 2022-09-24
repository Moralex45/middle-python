import uuid

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

    def unset(self, key: str):
        self.redis.delete(key)

    def set_user_session_by_user_id_and_user_agent(self,
                                                   user_id: uuid.UUID,
                                                   user_agent: str,
                                                   value: str,
                                                   expire_seconds: int):
        self.set(f'user_id::{user_id}::user_agent::{user_agent}',
                 value, expire_seconds * 60 * 60 * 60)

    def get_user_session_by_user_id_and_user_agent(self, user_id: uuid.UUID, user_agent: str) -> str | None:
        session = self.redis.get(f'user_id::{user_id}::user_agent::{user_agent}')

        return session

    def delete_user_session_by_user_id_and_user_agent(self, user_id: uuid.UUID, user_agent: str):
        self.unset(f'user_id::{user_id}::user_agent::{user_agent}')

    def get_user_sessions_by_user_id(self, user_id: uuid.UUID) -> [str]:
        return list(self.redis.scan_iter(f'user_id::{user_id}::user_agent::*'))

    def delete_user_sessions_by_user_id(self, user_id: uuid.UUID) -> [str]:
        keys = self.redis.keys(f'user_id::{user_id}::user_agent::*')
        if len(keys):
            self.redis.delete(*keys)
