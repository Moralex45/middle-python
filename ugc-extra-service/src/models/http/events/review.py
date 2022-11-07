from __future__ import annotations

import uuid

import pydantic

from src.models.base import Base


class ReviewCreation(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str


class Review(Base):
    id: uuid.UUID  # noqa: VNE003
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str
    publication_timestamp: int
    user_to_film_like: int | None = ...  # type:ignore
    average_review_mark: float | None = ...  # type:ignore

    @pydantic.validator('average_review_mark')
    def average_review_mark_check(cls, value: float | None):
        if value is not None:
            return round(value, 1)

        return None
