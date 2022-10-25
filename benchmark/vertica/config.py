from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    HOST: str = Field(env='VERTICA_HOST')
    PORT: int = Field(env='VERTICA_PORT')
    USER: str = Field(env='VERTICA_USER')
    PASSWORD: str = Field(env='VERTICA_PASSWORD')
    DATABASE: str = Field(env='VERTICA_DATABASE')
    AUTOCOMMIT: bool = Field(env='AUTOCOMMIT', default=True)
    READ_TIMEOUT: int = Field(env='READ_TIMEOUT')
    UNICODE_ERROR: str = Field(env='UNICODE_ERROR', default='strict')
    SSL: bool = Field(env='SSL', default=False)

    ROWS_NUMS: int = Field(env='ROWS_NUMS', default=1000000)
    CHUNK_SIZE: int = Field(env='CHUNK_SIZE', default=5000)

    class Config:
        __BASE_DIR_PATH = Path(__file__)
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


__settings = Settings()


@lru_cache
def get_settings_instance():
    return __settings
