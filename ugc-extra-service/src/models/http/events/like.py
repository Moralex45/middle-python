import uuid

from pydantic import Field

from src.models.inner.base import Base


class LikeCreation(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int
    device_fingerprint: str


class Like(Base):
    id: uuid.UUID = Field(..., alias='_id')  # noqa
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int
    device_fingerprint: str


class AverageLikeMarkByFilm(Base):
    mark: float
    amount: int
