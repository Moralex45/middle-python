import uuid

import src.models.http.base as base_http_models


class MovieWatchingEvent(base_http_models.Base):
    movie_id: uuid.UUID
    timeline: int  # Amount of seconds passed from movie start
    device_fingerprint: str
    user_id: uuid.UUID
