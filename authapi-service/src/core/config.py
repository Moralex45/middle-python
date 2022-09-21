from functools import lru_cache
# from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field, PostgresDsn

# from core.logger import LOGGING


class Settings(BaseSettings):
    # logging_config.dictConfig(LOGGING)

    PROJECT_NAME: str = Field(env='PROJECT_NAME')

    REDIS_HOST: str = Field(env='REDIS_HOST')
    REDIS_PORT: int = Field(env='REDIS_PORT')

    POSTGRES_SCHEMA: str = Field(env='POSTGRES_SCHEMA')
    POSTGRES_DSN: PostgresDsn = Field(env='POSTGRES_DSN')

    FLASK_HOST: str = Field(env='FLASK_HOST', default='127.0.0.1')
    FLASK_PORT: int = Field(env='FLASK_PORT', default=5000)

    JWT_SECRET_KEY: str = Field(env='JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(env='JWT_ACCESS_TOKEN_EXPIRES_SECONDS')
    JWT_COOKIE_SECURE: bool = Field(env='JWT_COOKIE_SECURE')

    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


__settings = Settings()


@lru_cache
def get_settings_instance():
    return __settings
