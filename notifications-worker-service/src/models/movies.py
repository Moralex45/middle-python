import uuid

from src.models.base import Base


class Movie(Base):
    id: uuid.UUID  # noqa: VNE003
    title: str
