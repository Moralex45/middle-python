from typing import Optional

from pydantic import BaseModel
from models.es_genres import ESGenre


class ESMoviePerson(BaseModel):
    id: str
    name: str


class ESMovie(BaseModel):
    id: str
    imdb_rating: Optional[float]
    genre: list[ESGenre]
    title: str
    description: Optional[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[ESMoviePerson]
    writers: list[ESMoviePerson]
    directors: list[ESMoviePerson]
