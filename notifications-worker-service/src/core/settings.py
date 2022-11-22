from enum import Enum
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


class AuthPostgresSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 5432
    db: str = 'auth_database'
    user: str = 'testuser'
    password: str = 'testpassword'

    class Config:
        env_prefix = 'AUTHPG_'

    @property
    def url(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class AdminPostgresSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 5432
    db: str = 'movies_database'
    user: str = 'testuser'
    password: str = 'testpassword'

    class Config:
        env_prefix = 'ADMINPG_'

    @property
    def url(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class ClickhouseSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 5469
    db: str = 'movies_db'
    user: str = 'testuser'
    password: str = 'testpassword'

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


class MailingSettings(BaseConfig):

    from_email: str = 'test@gmail.com'
    api_key: str = 'testapikey'

    class Config:
        env_prefix = 'MAILING_'


class ServicesPostgres(Enum):
    AUTH = 'auth'
    ADMIN = 'admin'


class ProjectSettings(BaseConfig):
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    auth_postgres: AuthPostgresSettings = AuthPostgresSettings()
    admin_postgres: AdminPostgresSettings = AdminPostgresSettings()
    clickhouse: ClickhouseSettings = ClickhouseSettings()
    mongo: MongoDBSettings = MongoDBSettings()
    mailing: MailingSettings = MailingSettings()
