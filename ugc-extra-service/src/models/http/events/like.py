import uuid

import pydantic

from src.models.http.base import Base


class LikeCreation(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int


class Like(Base):
    id: uuid.UUID  # noqa
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int


class AverageLikeMarkByFilm(Base):
    mark: float
    amount: int

    @pydantic.validator('mark')
    def mark_check(cls, value: float):
        return round(value, 1)
