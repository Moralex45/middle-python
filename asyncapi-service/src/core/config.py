from functools import lru_cache
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field

from core.logger import LOGGING


class Settings(BaseSettings):
    logging_config.dictConfig(LOGGING)

    PROJECT_NAME: str = Field(env='PROJECT_NAME', default='Movies async api')

    REDIS_HOST: str = Field(env='REDIS_HOST', default='127.0.0.1')
    REDIS_PORT: int = Field(env='REDIS_PORT', default=6379)

    ELASTIC_HOST = Field(env='ELASTIC_HOST', default='127.0.0.1')
    ELASTIC_PORT = Field(env='ELASTIC_PORT', default=9200)

    JWT_ACCESS_COOKIE_NAME: str = Field(env='JWT_ACCESS_COOKIE_NAME')
    REFRESH_TOKEN_COOKIE_NAME: str = Field(env='REFRESH_TOKEN_COOKIE_NAME')

    AUTH_SERVICE_TOKENS_REFRESH_URL: str = Field(env='AUTH_SERVICE_TOKENS_REFRESH_URL',
                                                 default='127.0.0.1:5000/api/v1/auth/refresh/body')

    DEBUG: bool = Field(env='DEBUG', default=False)

    FILM_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
    GENRE_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
    PERSON_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5

    @property
    def elastic_connection_url(self):
        return f'http://{self.ELASTIC_HOST}:{self.ELASTIC_PORT}'

    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


__settings = Settings()


@lru_cache
def get_settings_instance():
    return __settings
