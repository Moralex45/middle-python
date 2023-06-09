import uuid

import src.models.http.base as base_http_models


class BaseEvent(base_http_models.Base):
    device_fingerprint: str
    user_id: uuid.UUID


class MovieWatchingEventRequestBody(BaseEvent):
    movie_id: uuid.UUID
    timeline: int  # Amount of seconds passed from movie start
