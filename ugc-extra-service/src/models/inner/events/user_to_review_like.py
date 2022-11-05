import uuid

import pydantic

from src.models.base import Base


class UserToReviewLike(Base):
    id: uuid.UUID = pydantic.Field(..., alias='_id')  # noqa: VNE003
    user_id: uuid.UUID
    review_id: uuid.UUID
    mark: int

    def to_dict(self, by_alias: bool = True) -> dict:
        data = self.dict(by_alias=by_alias)
        data['_id' if by_alias else 'id'] = str(self.id)
        data['review_id'] = str(self.review_id)
        data['user_id'] = str(self.user_id)

        return data
