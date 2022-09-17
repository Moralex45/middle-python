from abc import ABC, abstractmethod

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel, ABC):
    ...

    class Config:
        orm_mode = True
        # json_loads = orjson.loads
        # json_dumps = orjson_dumps
