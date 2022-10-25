from fastapi import Query
from pydantic import BaseModel


class PaginatedParams(BaseModel):
    page_size: int
    page_number: int

    @classmethod
    async def query_paginated_parameters(cls,
                                         page_size: int = Query(default=50, alias='page[size]', ge=1),
                                         page_number: int = Query(default=1, alias='page[number]', ge=1)):
        return cls(page_size=page_size, page_number=page_number)
