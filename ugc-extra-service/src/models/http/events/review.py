from __future__ import annotations

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
    user_to_film_like: int | None
    average_review_mark: float | None
