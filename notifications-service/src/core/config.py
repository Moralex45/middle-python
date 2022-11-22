from __future__ import annotations

import functools
from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


class MongodbSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 27017

    mongodb_database: str = 'notifications'
    events_notifications_collection: str = 'events'
    admin_notifications_collection: str = 'admin'

    class Config:
        env_prefix = 'MONGODB_'

    @property
    def url(self):
        return f'{self.host}:{self.port}'


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


class SentrySettings(BaseConfig):
    dsn: str = ''

    class Config:
        env_prefix = 'SENTRY_'


class ProjectSettings(BaseConfig):
    mongodb_settings: MongodbSettings = MongodbSettings()
    rabbitmq_settings: RabbitMQSettings = RabbitMQSettings()
    sentry_settings: SentrySettings = SentrySettings()

    project_name: str = 'Notification service'

    debug: bool = False


__settings = ProjectSettings()


@functools.lru_cache()
def get_settings() -> ProjectSettings:
    return __settings
