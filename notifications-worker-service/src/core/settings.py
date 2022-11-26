import typing
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings


LogLevel = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']


class EventTypes(Enum):
    LIKES = 'likes'
    REGISTRATION = 'registration'
    NEW_SERIES = 'new_series'
    MAILING = 'mailing'


class ServicesPostgres(Enum):
    AUTH = 'auth'
    ADMIN = 'admin'


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
    prefetch_count: int = 1

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

    batch_size: int = 10_000
    user_info_table_name: str = 'users_data'

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

    batch_size: int = 10_000
    movie_table_name: str = 'film_work'

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

    batch_size: int = 10_000
    db_table: str = 'movie_timelines'

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


class TemplatesSettings(BaseConfig):

    likes_event_path: Path = Path(__file__).parent.parent / 'templates' / 'likes.html'
    registration_event_path: Path = Path(__file__).parent.parent / 'templates' / 'registration.html'
    new_series_event_path: Path = Path(__file__).parent.parent / 'templates' / 'new_series.html'
    mass_mailing_event_path: Path = Path(__file__).parent.parent / 'templates' / 'mass_mailing.html'

    likes_subject: str = 'Ваш отзыв оценили'
    registration_subject: str = 'Подтвердите регистрацию'
    new_series_subject: str = 'Вышла новая серия сериала'

    def get_templates_path(self, name: EventTypes) -> Path:
        match name:
            case EventTypes.LIKES:
                return self.likes_event_path
            case EventTypes.MAILING:
                return self.mass_mailing_event_path
            case EventTypes.NEW_SERIES:
                return self.new_series_event_path
            case EventTypes.REGISTRATION:
                return self.registration_event_path

    def get_subject(self, name: EventTypes) -> str:
        match name:
            case EventTypes.LIKES:
                return self.likes_subject
            case EventTypes.NEW_SERIES:
                return self.new_series_subject
            case EventTypes.REGISTRATION:
                return self.registration_subject
            case EventTypes.MAILING:
                return ''

    class Config:
        env_prefix = 'TMPL_'


class EventWorkerSettings(BaseConfig):
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    auth_postgres: AuthPostgresSettings = AuthPostgresSettings()
    admin_postgres: AdminPostgresSettings = AdminPostgresSettings()
    clickhouse: ClickhouseSettings = ClickhouseSettings()
    mongo: MongoDBSettings = MongoDBSettings()

    LOGS_MIN_LEVEL: LogLevel = 'DEBUG'
    LOGS_FORMAT: str = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'


class MessageWorkerSettings(BaseConfig):
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    mailing: MailingSettings = MailingSettings()
    templates: TemplatesSettings = TemplatesSettings()

    LOGS_MIN_LEVEL: LogLevel = 'DEBUG'
    LOGS_FORMAT: str = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
