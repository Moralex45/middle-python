from uuid import UUID

from models.base import Base


class PersonBase(Base):
    uuid: UUID
    full_name: str

    @classmethod
    def from_es(cls, **kwargs):
        return cls(
            uuid=kwargs['id'],
            full_name=kwargs['name'],
        )


class Person(PersonBase):
    role: list[str]
    film_ids: list[UUID]

    @classmethod
    def from_es(cls, **kwargs):
        return cls(
            uuid=kwargs['id'],
            full_name=kwargs['full_name'],
            role=kwargs['role'],
            film_ids=kwargs['film_ids'],
        )
