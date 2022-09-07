import asyncio

import pytest
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import TestSettings
from tests.functional.testdata import es_mapping
from tests.functional.testdata.data_to_elastic import data_for_elastic


@pytest.fixture(scope='session')
async def es_client(settings_instance: TestSettings):
    client = AsyncElasticsearch(hosts=[settings_instance.elasticsearch_connection_url])
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def create_index(es_client: AsyncElasticsearch, settings_instance: TestSettings):
    await es_client.indices.delete(index='_all')
    await es_client.indices.create(index=settings_instance.movies_elastic_search_index_name,
                                   body=es_mapping.MOVIES_INDEX_BODY)
    await es_client.indices.create(index=settings_instance.genres_elastic_search_index_name,
                                   body=es_mapping.GENRES_INDEX_BODY)
    await es_client.indices.create(index=settings_instance.persons_elastic_search_index_name,
                                   body=es_mapping.PERSONS_INDEX_BODY)
    await es_client.bulk(body=data_for_elastic())
    await asyncio.sleep(1)
    yield
    await es_client.indices.delete(index='_all')
