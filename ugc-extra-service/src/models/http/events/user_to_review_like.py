import uuid

import pydantic

from src.models.http.base import Base


class UserToReviewLikeCreation(Base):
    user_id: uuid.UUID
    review_id: uuid.UUID
    mark: int

    @pydantic.validator('mark')
    def mark_check(cls, value: int):
        if not (0 <= value <= 10):
            raise ValueError('mark diapason: [1; 10]')

        return value


class UserToReviewLike(Base):
    id: uuid.UUID  # noqa
    user_id: uuid.UUID
    review_id: uuid.UUID
    mark: int
