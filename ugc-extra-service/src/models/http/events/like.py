import uuid

import pydantic

from src.models.http.base import Base


class UserToFilmLikeCreation(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int


class UserToFilmLike(Base):
    id: uuid.UUID  # noqa
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int


class AverageUserToFilmMarkByFilm(Base):
    mark: float
    amount: int

    @pydantic.validator('mark')
    def mark_check(cls, value: float):
        return round(value, 1)
