from abc import ABC, abstractmethod

import orjson
from pydantic import BaseModel


def orjson_dumps(value, *, default):
    return orjson.dumps(value, default=default).decode()


class Base(BaseModel, ABC):
    """
        Базовый класс для моделей API
    """

    @classmethod
    @abstractmethod
    def from_es(cls, **kwargs):
        raise NotImplementedError()

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
