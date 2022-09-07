import uuid
import pytest
from http import HTTPStatus
from tests.functional.settings import get_settings_instance
from tests.functional.testdata.data_to_elastic import persons, movies
from tests.functional.src.tools import transform_person_test_data, prepare_person_film_data


@pytest.mark.asyncio
async def test_get_person_detailed(create_index, make_get_request):
    out_test_data = transform_person_test_data(persons[0])
    person_id = out_test_data['uuid']
    response = await make_get_request(f'/persons/{person_id}', params={})
    assert response.status == HTTPStatus.OK
    assert response.body['uuid'] == person_id
    assert response.body['full_name'] == out_test_data['full_name']


@pytest.mark.asyncio
async def test_person_films(create_index, make_get_request):
    test_person_data = persons[0]
    test_movies_data = movies
    test_data_id = test_person_data['id']
    test_data_dict = {'id': test_data_id, 'name': test_person_data['full_name']}
    test_film_person_data = prepare_person_film_data(test_data_dict, test_movies_data)
    response = await make_get_request(f'/persons/{test_data_id}/film')
    assert response.status == HTTPStatus.OK
    assert response.body == test_film_person_data


@pytest.mark.asyncio
async def test_get_person_unknown(create_index, make_get_request):
    random_uuid = uuid.uuid4()
    response = await make_get_request(f'/persons/{random_uuid}')
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == 'person not found'


@pytest.mark.asyncio
async def test_cache_person(create_index, es_client, make_get_request, flush_db):
    random_uuid = uuid.uuid4()

    data = {
        'id': random_uuid,
        'full_name': 'James Test'
    }

    await es_client.create(
        get_settings_instance().persons_elastic_search_index_name,
        random_uuid,
        data
    )
    response_first = await make_get_request(f'/persons/{random_uuid}')
    assert response_first.status == HTTPStatus.OK
    await es_client.delete('persons', random_uuid)
    response_second = await make_get_request(f'/persons/{random_uuid}')
    assert response_second.status == HTTPStatus.OK
    assert response_first.body == response_second.body
