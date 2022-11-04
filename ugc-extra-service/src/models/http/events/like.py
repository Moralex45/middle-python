import uuid

from src.models.inner.base import Base


class Like(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int
    device_fingerprint: str
