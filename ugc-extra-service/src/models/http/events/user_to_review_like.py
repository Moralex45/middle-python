import uuid

from src.models.http.base import Base


class UserToReviewLikeCreation(Base):
    user_id: uuid.UUID
    review_id: uuid.UUID
    mark: int
