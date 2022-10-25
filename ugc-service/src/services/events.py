from functools import lru_cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from src.core.config import get_settings
from src.models.http.events import MovieWatchingEventRequestBody
from src.services.base import EventServiceInterface
from src.storages.kafka import get_kafka


class EventService(EventServiceInterface):
    def __init__(self, kafka: AIOKafkaProducer):
        self.kafka = kafka

    async def produce_movie_watching(self, event: MovieWatchingEventRequestBody):
        message_key = f'{event.user_id}+{event.movie_id}'
        await self.kafka.send(get_settings().MOVIE_WATCHING_EVENT_KAFKA_TOPIC,
                              key=message_key.encode(),
                              value=event.json().encode())


@lru_cache
def get_event_service(kafka: AIOKafkaProducer = Depends(get_kafka)) -> EventService:
    return EventService(kafka)
