from typing import Type

import backoff
from elasticsearch import AsyncElasticsearch, NotFoundError, exceptions

from db.storage.base import AsyncStorageService
from models import T


class AsyncElasticStorageService(AsyncStorageService):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic: AsyncElasticsearch = elastic

    @backoff.on_exception(backoff.expo, [exceptions.ConnectionError], max_time=10)
    async def get_by_id(self, id: str, base_class: Type[T], **kwargs) -> T | None:
        index: str = kwargs['index']

        try:
            doc = await self.elastic.get(index, id)
        except NotFoundError:
            return None
        return base_class.from_es(**doc['_source'])

    @backoff.on_exception(backoff.expo, [exceptions.ConnectionError], max_time=10)
    async def search(self, body: dict, base_class: Type[T], **kwargs) -> list[T] | None:
        index: str = kwargs['index']

        try:
            doc = await self.elastic.search(index=index, body=body)
        except NotFoundError:
            return None
        return [base_class.from_es(**hit['_source']) for hit in doc['hits']['hits']]

    async def close(self):
        await self.elastic.close()
