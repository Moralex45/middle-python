from pydantic import BaseModel


class ESPerson(BaseModel):
    id: str
    full_name: str
