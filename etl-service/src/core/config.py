from pathlib import Path

from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    postgres_schema: str = Field(env='POSTGRES_SCHEMA')
    pg_dsn: PostgresDsn = Field(env='POSTGRES_DSN')

    elasticsearch_host: str = Field(env='ELASTICSEARCH_HOST')
    elasticsearch_port: int = Field(env='ELASTICSEARCH_PORT')

    movies_elastic_search_index_name: str = Field(env='MOVIES_ELASTICSEARCH_INDEX')
    genres_elastic_search_index_name: str = Field(env='GENRES_ELASTICSEARCH_INDEX')
    persons_elastic_search_index_name: str = Field(env='PERSONS_ELASTICSEARCH_INDEX')

    load_batch_size: int = Field(env='LOAD_BATCH_SIZE')
    state_file_path: str = Field(env='STATE_FILE_PATH')
    main_cycle_sleep_time: int = Field(env='MAIN_CYCLE_SLEEP_TIME')

    @property
    def elasticsearch_connection_url(self):
        return f'http://{self.elasticsearch_host}:{self.elasticsearch_port}'

    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'
