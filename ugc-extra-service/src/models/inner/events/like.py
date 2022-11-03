import uuid

from pydantic import Field

from src.models.http.base import Base


class Like(Base):
    id: uuid.UUID = Field(..., alias='_id')  # noqa
    user_id: uuid.UUID
    movie_id: uuid.UUID
    device_fingerprint: str

    def to_dict(self, by_alias=True) -> dict:
        data = self.dict(by_alias=by_alias)
        data['_id'] = str(self.id)
        data['movie_id'] = str(self.movie_id)
        data['user_id'] = str(self.user_id)

        return data
