from __future__ import annotations

import functools
from pathlib import Path

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


class MongodbSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 27017

    mongodb_database: str = 'events'
    mongodb_likes_collection: str = 'likes'
    mongodb_reviews_collection: str = 'reviews'
    mongodb_bookmark_collection: str = 'bookmarks'

    class Config:
        env_prefix = 'MONGODB_'

    @property
    def url(self):
        return f'{self.host}:{self.port}'


class RedisSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 6379

    class Config:
        env_prefix = 'REDIS_'

    @property
    def url(self):
        return f'{self.host}:{self.port}'


class ProjectSettings(BaseConfig):
    mongodb_settings: MongodbSettings = MongodbSettings()
    redis_settings: RedisSettings = RedisSettings()

    project_name: str = 'UGC extra service'

    jwt_access_cookie_name: str = 'access_token_cookie'
    refresh_token_cookie_name: str = 'refresh_token_cookie'
    jwt_secret: str = Field(env='JWT_SECRET')
    auth_service_tokens_refresh_url: str = 'http://localhost:5000/api/v1/auth/refresh/body'

    debug: bool = False


__settings = ProjectSettings()


@functools.lru_cache()
def get_settings() -> ProjectSettings:
    return __settings
