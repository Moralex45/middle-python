import uuid

import pydantic

from src.models.base import Base


class UserToFilmLikeCreation(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int

    @pydantic.validator('mark')
    def mark_check(cls, value: int):
        if not (0 <= value <= 10):
            raise ValueError('mark diapason: [1; 10]')

        return value


class UserToFilmLike(Base):
    id: uuid.UUID  # noqa: VNE003
    user_id: uuid.UUID
    movie_id: uuid.UUID
    mark: int


class AverageUserToFilmMarkByFilm(Base):
    mark: float
    amount: int

    @pydantic.validator('mark')
    def mark_check(cls, value: float):
        return round(value, 1)
