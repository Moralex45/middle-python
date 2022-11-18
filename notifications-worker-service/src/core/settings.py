import functools
from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


class RabbitMQSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 5672
    username: str = 'guest'
    password: str = 'guest'

    routing_key: str = 'general_notification_queue'

    class Config:
        env_prefix = 'RABBITMQ_'

    @property
    def url(self):
        return f'amqp://{self.username}:{self.password}@{self.host}:{self.port}'


class PostgresSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 5469
    db: str = 'auth_database'
    user: str
    password: str

    class Config:
        env_prefix = 'PG_'

    @property
    def url(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class ClickhouseSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 5469
    db: str = 'movies_db'
    user: str
    password: str

    class Config:
        env_prefix = 'CH_'

    @property
    def url(self):
        return f'clickhouse://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class MongoDBSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 27017

    database: str = 'events'
    likes_collection: str = 'users_to_reviews_likes'

    class Config:
        env_prefix = 'MONGO_'

    @property
    def url(self):
        return f'{self.host}:{self.port}'


class ProjectSettings(BaseConfig):
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    postgres: PostgresSettings = PostgresSettings()
    clickhouse: ClickhouseSettings = ClickhouseSettings()
    mongo: MongoDBSettings = MongoDBSettings()


__settings = ProjectSettings()


@functools.lru_cache()
def get_settings() -> ProjectSettings:
    return __settings
