from faust import App
import backoff
from kafka.errors import KafkaConnectionError

from core.config import etl_logger, settings


@backoff.on_exception(backoff.expo,
                      exception=KafkaConnectionError,
                      logger=etl_logger,
                      max_time=10)
def get_faust_app():
    return App(
        'kafka-etl',
        broker=settings.kafka_settings.dsn,
        broker_commit_every=settings.kafka_settings.COMMIT_RECORDS,
        broker_commit_interval=settings.kafka_settings.COMMIT_SECONDS,
    )
