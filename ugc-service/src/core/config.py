from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


class KafKaSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 9092

    class Config:
        env_prefix = 'KAFKA_'

    @property
    def url(self):
        return f'{self.HOST}:{self.PORT}'


class RedisSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 6379

    class Config:
        env_prefix = 'REDIS_'

    @property
    def url(self):
        return f'{self.HOST}:{self.PORT}'


class ProjectSettings(BaseConfig):
    kafka_settings: KafKaSettings = KafKaSettings()
    redis_settings: RedisSettings = RedisSettings()

    PROJECT_NAME: str = 'UGC service'

    JWT_ACCESS_COOKIE_NAME: str = 'access_token_cookie'
    REFRESH_TOKEN_COOKIE_NAME: str = 'refresh_token_cookie'

    JWT_SECRET: str = Field(env='JWT_SECRET')

    AUTH_SERVICE_TOKENS_REFRESH_URL: str = 'http://localhost:5000/api/v1/auth/refresh/body'

    DEBUG: bool = False


__settings = ProjectSettings()


@lru_cache
def get_settings() -> ProjectSettings:
    return __settings
