import functools

import aiokafka
import fastapi

import src.repositories.events.kafka as kafka_repository
import src.services.kafka as kafka_service


@functools.lru_cache
def get_event_repository(
        kafka_instance: aiokafka.AIOKafkaProducer = fastapi.Depends(kafka_service.get_kafka),
) -> kafka_repository.KafkaEventRepository:
    return kafka_repository.KafkaEventRepository(kafka_instance)
