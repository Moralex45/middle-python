import uuid

from pydantic import BaseModel


class Message(BaseModel):
    id: uuid.UUID  # noqa: VNE003
    type: str  # noqa: VNE003
    content: dict
