import aiokafka

import src.core.config as project_config
import src.models.inner.events as inner_events_models
import src.repositories.events.base as base_repositories


class KafkaEventRepository(base_repositories.EventRepositoryProtocol):
    def __init__(self, kafka: aiokafka.AIOKafkaProducer):
        self.kafka = kafka

    async def produce(self, event: inner_events_models.MovieWatchingEvent) -> None:
        message_key = f'{event.user_id}+{event.movie_id}'
        await self.kafka.send(project_config.get_settings().movie_watching_event_kafka_topic,
                              key=message_key.encode(),
                              value=event.json().encode())
