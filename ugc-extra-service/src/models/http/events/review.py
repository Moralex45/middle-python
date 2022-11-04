import uuid

from src.models.http.base import Base


class ReviewCreation(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str
    publication_timestamp: int


class Review(Base):
    id: uuid.UUID  # noqa
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str
    publication_timestamp: int
    average_mark: float | None
