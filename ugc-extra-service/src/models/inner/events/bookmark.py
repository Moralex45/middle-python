import uuid

from pydantic import Field

from src.models.base import Base


class Bookmark(Base):
    id: uuid.UUID = Field(..., alias='_id')  # noqa: VNE003
    user_id: uuid.UUID
    movie_id: uuid.UUID

    def to_dict(self, by_alias: bool = True) -> dict:
        data = self.dict(by_alias=by_alias)
        data['_id' if by_alias else 'id'] = str(self.id)
        data['movie_id'] = str(self.movie_id)
        data['user_id'] = str(self.user_id)

        return data
