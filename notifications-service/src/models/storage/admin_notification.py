from __future__ import annotations

import uuid

import pydantic

from src.models.base import Base


class ServiceNotification(Base):
    id: uuid.UUID = pydantic.Field(..., alias='_id')  # noqa: VNE003
    type: str  # noqa: VNE003
    content: str
    recepients: list
    sending_time_timestamp: int | None
    sending_timeout: int | None

    def to_dict(self, by_alias: bool = True) -> dict:
        data = self.dict(by_alias=by_alias)
        data['_id' if by_alias else 'id'] = str(self.id)

        return data
