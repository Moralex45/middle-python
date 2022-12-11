import uuid

from src.models.base import Base
from src.core.settings import EventTypes


class EventMessage(Base):
    id: uuid.UUID  # noqa: VNE003
    type: EventTypes  # noqa: VNE003
    content: dict


class PersonalizedMessage(Base):
    id: uuid.UUID  # noqa: VNE003
    type: EventTypes  # noqa: VNE003
    email: str
    content: dict
