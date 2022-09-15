from typing import TypeVar

from models.film import Film, FilmBase
from models.genre import Genre
from models.person import Person, PersonBase

T = TypeVar('T', Film, FilmBase, Genre, Person, PersonBase)
