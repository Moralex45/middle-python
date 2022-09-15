from functools import lru_cache
# from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field

# from core.logger import LOGGING


class Settings(BaseSettings):
    # logging_config.dictConfig(LOGGING)

    PROJECT_NAME: str = Field(env='PROJECT_NAME', default='auth-api')

    REDIS_HOST: str = Field(env='REDIS_HOST', default='127.0.0.1')
    REDIS_PORT: int = Field(env='REDIS_PORT', default=6379)

    POSTGRES_DB_NAME: str = Field(env='DB_NAME', default='auth')
    POSTGRES_DB_USER: str = Field(env='DB_USER', default='app')
    POSTGRES_DB_PASSWORD: str = Field(env='DB_PASSWORD', default='123qwe')
    POSTGRES_DB_HOST: str = Field(env='DB_HOST', default='127.0.0.1')
    POSTGRES_DB_PORT: int = Field(env='DB_PORT', default=54320)

    FLASK_HOST: str = Field(env='FLASK_HOST', default='127.0.0.1')
    FLASK_PORT: int = Field(env='FLASK_PORT', default=5000)

    JWT_SECRET_KEY: str = Field(env='JWT_SECRET_KEY', default='secret')

    @property
    def postgres_connection_url(self):
        return f'postgresql+psycopg2://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}'  # noqa

    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


__settings = Settings()


@lru_cache
def get_settings_instance():
    return __settings
