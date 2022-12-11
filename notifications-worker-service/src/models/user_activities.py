import uuid

from src.models.base import Base


class Review(Base):
    id: uuid.UUID  # noqa: VNE003
    user_id: uuid.UUID  # noqa: VNE003
    movie_id: uuid.UUID
