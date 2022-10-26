import functools

import aiokafka

kafka_instance: aiokafka.AIOKafkaProducer | None = None


@functools.lru_cache
def get_kafka() -> aiokafka.AIOKafkaProducer:
    return kafka_instance
