from __future__ import annotations

import uuid

import pydantic

from src.models.http.base import Base


class Review(Base):
    id: uuid.UUID = pydantic.Field(..., alias='_id')  # noqa: VNE003
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str
    publication_timestamp: int

    def to_dict(self, by_alias: bool = True) -> dict:
        data = self.dict(by_alias=by_alias)
        data['_id' if by_alias else 'id'] = str(self.id)
        data['movie_id'] = str(self.movie_id)
        data['user_id'] = str(self.user_id)

        return data
