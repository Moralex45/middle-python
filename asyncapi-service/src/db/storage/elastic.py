import backoff
from elasticsearch import AsyncElasticsearch, NotFoundError, exceptions

from db.storage import AsyncStorageService
from models.base import Base


class AsyncElasticStorageService(AsyncStorageService):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic: AsyncElasticsearch = elastic

    @backoff.on_exception(backoff.expo, [exceptions.ConnectionError], max_time=10)
    async def get_by_id(self, **kwargs) -> Base | None:
        index: str = kwargs['index']
        base_class: Base = kwargs['base_class']
        _id: str = kwargs['id']

        try:
            doc = await self.elastic.get(index, _id)
        except NotFoundError:
            return None
        return base_class.from_es(**doc['_source'])

    @backoff.on_exception(backoff.expo, [exceptions.ConnectionError], max_time=10)
    async def search(self, **kwargs) -> list[Base] | None:
        index: str = kwargs['index']
        base_class: Base = kwargs['base_class']
        body: dict = kwargs['body']

        try:
            doc = await self.elastic.search(index=index, body=body)
        except NotFoundError:
            return None
        return [base_class.from_es(**hit['_source']) for hit in doc['hits']['hits']]

    async def close(self):
        await self.elastic.close()
