from uuid import UUID

from models.base import Base


class Genre(Base):
    uuid: UUID
    name: str

    @classmethod
    def from_es(cls, **kwargs):
        return cls(uuid=kwargs['id'], name=kwargs['name'])
