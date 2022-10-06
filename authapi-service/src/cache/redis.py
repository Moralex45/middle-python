import uuid

import redis

from src.cache.base import CacheService


class RedisCacheService(CacheService):
    def __init__(self, redis_instance: redis.Redis):
        self.redis: redis.Redis = redis_instance

    def get(self, key: str) -> str | None:
        data = self.redis.get(key)
        if not data:
            return None

        return data

    def set(self, key: str, value: str, expire: int):
        self.redis.setex(key, expire, value)

    def unset(self, key: str):
        self.redis.delete(key)

    def set_with_pipeline(self, key: str, value: str, expire: int = None):
        pipe = self.redis.pipeline()
        pipe.set(key, value)
        if expire:
            pipe.expire(key, expire)
        pipe.execute()

    def get_address_requests_amount(self,
                                    remote_address: str,
                                    minute_value: int) -> int | None:
        amount = self.get(f'remote_address::{remote_address}::minute::{minute_value}')

        return int(amount) if amount is not None else amount

    def set_address_requests_amount(self,
                                    remote_address: str,
                                    minute_value: int,
                                    value: str):
        self.set(f'remote_address::{remote_address}::minute::{minute_value}', value, minute_value)

    def increment_address_requests_amount(self,
                                          remote_address: str,
                                          minute_value: int):
        amount = self.get_address_requests_amount(remote_address, minute_value)
        self.set_with_pipeline(f'remote_address::{remote_address}::minute::{minute_value}', str(amount+1), minute_value)

    def set_user_session_by_user_id_and_user_agent(self,
                                                   user_id: uuid.UUID,
                                                   user_agent: str,
                                                   value: str,
                                                   expire_seconds: int):
        self.set(f'user_id::{user_id}::user_agent::{user_agent}',
                 value, expire_seconds * 60 * 60 * 60)

    def get_user_session_by_user_id_and_user_agent(self, user_id: uuid.UUID, user_agent: str) -> str | None:
        session = self.get(f'user_id::{user_id}::user_agent::{user_agent}')

        return session

    def delete_user_session_by_user_id_and_user_agent(self, user_id: uuid.UUID, user_agent: str):
        self.unset(f'user_id::{user_id}::user_agent::{user_agent}')

    def get_user_sessions_by_user_id(self, user_id: uuid.UUID) -> [str]:
        return self.redis.mget(list(self.redis.scan_iter(f'user_id::{user_id}::user_agent::*')))

    def delete_user_sessions_by_user_id(self, user_id: uuid.UUID) -> [str]:
        keys = self.redis.keys(f'user_id::{user_id}::user_agent::*')
        if len(keys):
            self.redis.delete(*keys)
