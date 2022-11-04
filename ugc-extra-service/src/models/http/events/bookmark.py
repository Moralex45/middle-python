import uuid

from src.models.http.base import Base


class BookmarkCreation(Base):
    user_id: uuid.UUID
    movie_id: uuid.UUID


class Bookmark(Base):
    id: uuid.UUID  # noqa
    user_id: uuid.UUID
    movie_id: uuid.UUID
