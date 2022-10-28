from pydantic import BaseModel


class ESGenre(BaseModel):
    id: str
    name: str
