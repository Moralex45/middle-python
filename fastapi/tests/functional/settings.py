from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    REDIS_HOST: str = Field(env='REDIS_HOST', default='127.0.0.1')
    REDIS_PORT: int = Field(env='REDIS_PORT', default=6379)

    ELASTIC_HOST: str = Field(env='ELASTIC_HOST', default='127.0.0.1')
    ELASTIC_PORT = Field(env='ELASTIC_PORT', default=9200)

    BASE_API: str = Field(env='BASE_API', default='http://127.0.0.1:8000')

    movies_elastic_search_index_name: str = Field(env='MOVIES_ELASTICSEARCH_INDEX', default='movies')
    genres_elastic_search_index_name: str = Field(env='GENRES_ELASTICSEARCH_INDEX', default='genres')
    persons_elastic_search_index_name: str = Field(env='PERSONS_ELASTICSEARCH_INDEX', default='persons')

    @property
    def elasticsearch_connection_url(self):
        return f'http://{self.ELASTIC_HOST}:{self.ELASTIC_PORT}'

    class Config:
        __BASE_DIR_PATH = Path(__file__)
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


__settings = TestSettings()


@lru_cache
def get_settings_instance():
    return __settings
