from abc import ABC, abstractmethod

import src.models.inner.events as inner_events_models


class EventRepositoryProtocol(ABC):
    @abstractmethod
    async def produce(self, event: inner_events_models.MovieWatchingEvent) -> None:
        raise NotImplementedError
