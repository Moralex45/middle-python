from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
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
    APP_SECRET_KEY: str = Field(env='APP_SECRET_KEY')

    JWT_SECRET_KEY: str = Field(env='JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(env='JWT_ACCESS_TOKEN_EXPIRES_SECONDS')
    JWT_COOKIE_SECURE: bool = Field(env='JWT_COOKIE_SECURE')
    JWT_ACCESS_COOKIE_NAME: str = Field(env='JWT_ACCESS_COOKIE_NAME')

    REFRESH_TOKEN_COOKIE_NAME: str = Field(env='REFRESH_TOKEN_COOKIE_NAME')
    REFRESH_TOKEN_EXPIRES_LONG: int = Field(env='REFRESH_TOKEN_EXPIRES_LONG_DAYS')
    REFRESH_TOKEN_EXPIRES_SHORT: int = Field(env='REFRESH_TOKEN_EXPIRES_SHORT_DAYS')

    # Yandex
    YANDEX_ID: str = Field(env='YANDEX_ID')
    YANDEX_SECRET: str = Field(env='YANDEX_SECRET')
    YANDEX_AUTHORIZE_URL: str = Field(env='YANDEX_AUTHORIZE_URL')
    YANDEX_TOKEN_URL: str = Field(env='YANDEX_TOKEN_URL')
    YANDEX_PROFILE_URL: str = Field(env='YANDEX_PROFILE_URL')

    USER_REQUEST_LIMIT_PER_MINUTE: int = Field(env='USER_REQUEST_LIMIT_PER_MINUTE')

    JAEGER_HOST: str = Field(env="JAEGER_HOST")
    JAEGER_PORT: int = Field(env="JAEGER_PORT")

    ENABLE_TRACER: bool = Field(env='ENABLE_TRACER')
    ENABLE_DDOS_PROTECTION: bool = Field(env='ENABLE_DDOS_PROTECTION')

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
