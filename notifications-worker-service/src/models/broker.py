import uuid

from src.models.base import Base


class Message(Base):
    id: uuid.UUID  # noqa: VNE003
    type: str  # noqa: VNE003
    content: dict
