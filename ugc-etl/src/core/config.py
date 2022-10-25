from logging import Logger

from pydantic import BaseConfig, BaseSettings
from pydantic import KafkaDsn


class KafkaSettings(BaseConfig):
    HOST: str = '127.0.0.1'
    PORT: int = 9092

    class Config:
        env_prefix = 'KAFKA_'

    @property
    def dsn(self) -> KafkaDsn:
        dsn: KafkaDsn = f'kafka://{self.HOST}:{self.PORT}'
        return dsn


class CHSettings(BaseConfig):
    HOST: str = '127.0.0.1'
    PORT: int = 9000
    USER: str = 'admin'
    PASSWORD: str = 'password'
    DATABASE: str = 'movies_db'

    class Config:
        env_prefix = 'CH_'

    @property
    def dsn(self) -> str:
        return f'clickhouse://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'


class Settings(BaseSettings):
    kafka_settings = KafkaSettings()
    ch_settings = CHSettings()


settings = Settings()
etl_logger = Logger('UGC ETL logger')
