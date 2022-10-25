import uuid

from src.models.http.base import Base


class BaseEvent(Base):
    device_fingerprint: str
    user_id: uuid.UUID


class MovieWatchingEventRequestBody(BaseEvent):
    movie_id: uuid.UUID
    timeline: int  # Amount of seconds passed from movie start
