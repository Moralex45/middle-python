import pytest
import pytest_asyncio
from aiokafka import AIOKafkaConsumer


@pytest_asyncio.fixture(scope='session')
async def __get_async_kafka_client(event_loop, get_server_settings_instance) -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        get_server_settings_instance.movie_watching_event_kafka_topic,
        loop=event_loop,
        bootstrap_servers=get_server_settings_instance.kafka_settings.url
    )
    await consumer.start()
    yield consumer
    await consumer.stop()


@pytest.fixture(scope='session')
def get_kafka_client(__get_async_kafka_client) -> AIOKafkaConsumer:
    return __get_async_kafka_client
