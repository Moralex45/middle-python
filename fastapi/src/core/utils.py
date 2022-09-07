from abc import ABC, abstractmethod
from typing import Any, Type

import orjson
from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder

from models.base import Base


class Serializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize(obj: Any) -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def deserialize(data: str, base_class: Type) -> Any:
        raise NotImplementedError()


class PydanticModelSerializer(Serializer):
    @staticmethod
    def serialize(obj: Base) -> str:
        return obj.json()

    @staticmethod
    def deserialize(data: str, base_class: Type[Base]) -> Any:
        base_class.parse_raw(data)


class PydanticModelListSerializer(Serializer):
    @staticmethod
    def serialize(obj: list[Base]) -> str:
        return orjson.dumps(obj, default=pydantic_encoder).decode()

    @staticmethod
    def deserialize(data: str, base_class: Type[Base]) -> Any:
        parse_obj_as(list[base_class], orjson.loads(data))
