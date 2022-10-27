from uuid import UUID

from pydantic import BaseModel


class View(BaseModel):
    user_id: UUID
    film_id: UUID
    device_fingerprint: str
    timeline: float
