import uuid

from src.models.http.base import Base


class Like(Base):
    _id: uuid.UUID
    user_id: uuid.UUID
    movie_id: uuid.UUID
    device_fingerprint: str
