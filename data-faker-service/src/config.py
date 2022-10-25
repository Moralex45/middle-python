from pathlib import Path

from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    POSTGRES_SCHEMA: str = Field(env='POSTGRES_SCHEMA')

    POSTGRES_DB_NAME: str = Field(env='DB_NAME')
    POSTGRES_DB_USER: str = Field(env='DB_USER')
    POSTGRES_DB_PASSWORD: str = Field(env='DB_PASSWORD')
    POSTGRES_DB_HOST: str = Field(env='DB_HOST')
    POSTGRES_DB_PORT: int = Field(env='DB_PORT')

    LOAD_BATCH_SIZE: int = Field(env='LOAD_BATCH_SIZE')

    GENRES_AMOUNT: int = Field(env='GENRES_AMOUNT')
    PERSONS_AMOUNT: int = Field(env='PERSONS_AMOUNT')
    FILMWORKS_MOVIES_AMOUNT: int = Field(env='FILMWORKS_MOVIES_AMOUNT')
    FILMWORKS_TV_SHOWS_AMOUNT: int = Field(env='FILMWORKS_TV_SHOWS_AMOUNT')

    GENRES_TO_FILMWORK_MIN_AMOUNT: int = Field(env='GENRES_TO_FILMWORK_MIN_AMOUNT')
    GENRES_TO_FILMWORK_MAX_AMOUNT: int = Field(env='GENRES_TO_FILMWORK_MAX_AMOUNT')

    DIRECTORS_TO_FILMWORKS_MIN_AMOUNT: int = Field(env='DIRECTORS_TO_FILMWORK_MIN_AMOUNT')
    DIRECTORS_TO_FILMWORKS_MAX_AMOUNT: int = Field(env='DIRECTORS_TO_FILMWORK_MAX_AMOUNT')

    ACTORS_TO_FILMWORKS_MIN_AMOUNT: int = Field(env='ACTORS_TO_FILMWORK_MIN_AMOUNT')
    ACTORS_TO_FILMWORKS_MAX_AMOUNT: int = Field(env='ACTORS_TO_FILMWORK_MAX_AMOUNT')

    WRITERS_TO_FILMWORKS_MIN_AMOUNT: int = Field(env='WRITERS_TO_FILMWORK_MIN_AMOUNT')
    WRITERS_TO_FILMWORKS_MAX_AMOUNT: int = Field(env='WRITERS_TO_FILMWORK_MAX_AMOUNT')

    @property
    def postgres_dsn(self) -> str:
        return f'postgresql://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}' \
               f'@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}'

    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'
