from functools import lru_cache
# from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field

# from core.logger import LOGGING


class Settings(BaseSettings):
    # logging_config.dictConfig(LOGGING)

    PROJECT_NAME: str = Field(env='PROJECT_NAME')

    REDIS_HOST: str = Field(env='REDIS_HOST')
    REDIS_PORT: int = Field(env='REDIS_PORT')

    POSTGRES_SCHEMA: str = Field(env='POSTGRES_SCHEMA')
    POSTGRES_DB_HOST: str = Field(env='POSTGRES_DB_HOST')
    POSTGRES_DB_PORT: int = Field(env='POSTGRES_DB_PORT')
    POSTGRES_DB_NAME: str = Field(env='POSTGRES_DB_NAME')
    POSTGRES_DB_USER: str = Field(env='POSTGRES_DB_USER')
    POSTGRES_DB_PASSWORD: str = Field(env='POSTGRES_DB_PASSWORD')

    FLASK_HOST: str = Field(env='FLASK_HOST', default='127.0.0.1')
    FLASK_PORT: int = Field(env='FLASK_PORT', default=5000)

    JWT_SECRET_KEY: str = Field(env='JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(env='JWT_ACCESS_TOKEN_EXPIRES_SECONDS')
    JWT_COOKIE_SECURE: bool = Field(env='JWT_COOKIE_SECURE')
    JWT_ACCESS_COOKIE_NAME: str = Field(env='JWT_ACCESS_COOKIE_NAME')

    REFRESH_TOKEN_COOKIE_NAME: str = Field(env='REFRESH_TOKEN_COOKIE_NAME')
    REFRESH_TOKEN_EXPIRES_LONG: int = Field(env='REFRESH_TOKEN_EXPIRES_LONG_DAYS')
    REFRESH_TOKEN_EXPIRES_SHORT: int = Field(env='REFRESH_TOKEN_EXPIRES_SHORT_DAYS')

    @property
    def POSTGRES_DSN(self) -> str:
        return f'postgresql+psycopg2://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}' \
               f'@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}'

    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


__settings = Settings()


@lru_cache
def get_settings_instance():
    return __settings
