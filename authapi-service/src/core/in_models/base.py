from abc import ABC

from pydantic import BaseModel


class Base(BaseModel, ABC):
    ...
