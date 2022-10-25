from typing import Optional
from uuid import UUID

from models.base import Base
from models.genre import Genre
from models.person import PersonBase


class FilmBase(Base):
    uuid: UUID
    title: str
    imdb_rating: Optional[float]

    @classmethod
    def from_es(cls, **kwargs):
        return cls(uuid=kwargs['id'], title=kwargs['title'], imdb_rating=kwargs['imdb_rating'])


class Film(FilmBase):
    description: Optional[str]
    genre: list[Genre]
    actors: Optional[list[PersonBase]]
    writers: Optional[list[PersonBase]]
    directors: Optional[list[PersonBase]]

    @classmethod
    def from_es(cls, **kwargs):
        return cls(
            uuid=kwargs['id'],
            title=kwargs['title'],
            imdb_rating=kwargs['imdb_rating'],
            genre=[Genre.from_es(**genre) for genre in kwargs['genre']],
            actors=[PersonBase.from_es(**actor) for actor in kwargs['actors']],
            writers=[PersonBase.from_es(**writer) for writer in kwargs['writers']],
            directors=[PersonBase.from_es(**director) for director in kwargs['directors']],
        )
