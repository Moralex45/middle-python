from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings


class BaseConfig(BaseSettings):

    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


class KafKaSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 9092

    class Config:
        env_prefix = 'KAFKA_'

    @property
    def url(self):
        return f'{self.HOST}:{self.PORT}'


class ProjectSettings(BaseConfig):

    PROJECT_NAME: str = 'UGC service'
    SECRET: str = 'aslkdklervoer[gjadlgke'
    kafka: KafKaSettings = KafKaSettings()


__settings = ProjectSettings()


@lru_cache
def get_settings() -> ProjectSettings:
    return __settings
