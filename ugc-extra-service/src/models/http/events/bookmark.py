import uuid

from src.models.base import Base


class BookmarkCreation(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID


class Bookmark(Base):
    id: uuid.UUID  # noqa: VNE003
    user_id: uuid.UUID
    movie_id: uuid.UUID
