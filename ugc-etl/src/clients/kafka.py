from faust import App
import backoff
from kafka.errors import KafkaConnectionError

from core.config import etl_logger, settings


@backoff.on_exception(backoff.expo,
                      exception=KafkaConnectionError,
                      logger=etl_logger,
                      max_time=10)
def get_faust_app():
    app = App('kafka-etl', broker=settings.kafka_settings.dsn)
    return app
