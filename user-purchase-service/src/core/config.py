from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    PROJECT_NAME: str = Field(env='PROJECT_NAME', default='user-purchase-service')
    DEBUG: bool = Field(env='DEBUG', default=False)

    POSTGRES_SCHEMA: str = Field(env='POSTGRES_SCHEMA')
    POSTGRES_DB_HOST: str = Field(env='POSTGRES_DB_HOST')
    POSTGRES_DB_PORT: int = Field(env='POSTGRES_DB_PORT')
    POSTGRES_DB_NAME: str = Field(env='POSTGRES_DB_NAME')
    POSTGRES_DB_USER: str = Field(env='POSTGRES_DB_USER')
    POSTGRES_DB_PASSWORD: str = Field(env='POSTGRES_DB_PASSWORD')

    APP_HOST: str = Field(env='APP_HOST', default='127.0.0.1')
    APP_PORT: int = Field(env='APP_PORT', default=5000)
    BILLING_SERVICE_URL: str = 'http://localhost:8000'

    @property
    def POSTGRES_DSN(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}' \
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
