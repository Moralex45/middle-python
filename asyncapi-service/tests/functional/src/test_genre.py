import uuid
import pytest
from http import HTTPStatus
from tests.functional.testdata.data_to_elastic import genres
from tests.functional.settings import get_settings_instance
from tests.functional.src.tools import transform_genre_test_data, transform_genre_list_test_data


@pytest.mark.asyncio
async def test_get_genre_detailed(create_index, make_get_request):
    out_test_data = transform_genre_test_data(genres[0])
    genre_id = out_test_data['uuid']
    response = await make_get_request(f'/genres/{genre_id}', params={})
    assert response.status == HTTPStatus.OK
    assert response.body['uuid'] == genre_id
    assert response.body['name'] == out_test_data['name']


@pytest.mark.asyncio
async def test_get_all_genres(create_index, make_get_request):
    response = await make_get_request('/genres/', params={})
    assert response.status == HTTPStatus.OK
    out_test_data = transform_genre_list_test_data(genres)
    assert response.body == out_test_data


@pytest.mark.asyncio
async def test_get_genre_unknown(create_index, make_get_request):
    random_uuid = uuid.uuid4()
    response = await make_get_request(f'/genres/{random_uuid}')
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == 'genre not found'


@pytest.mark.asyncio
async def test_cache_genre(create_index, es_client, make_get_request, flush_db):
    random_uuid = uuid.uuid4()

    data = {
        'id': random_uuid,
        'name': 'TestName'
    }

    await es_client.create(
        get_settings_instance().genres_elastic_search_index_name,
        random_uuid,
        data
    )
    response_first = await make_get_request(f'/genres/{random_uuid}')
    assert response_first.status == HTTPStatus.OK
    await es_client.delete('genres', random_uuid)
    response_second = await make_get_request(f'/genres/{random_uuid}')
    assert response_second.status == HTTPStatus.OK
    assert response_first.body == response_second.body
