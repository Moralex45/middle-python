import uuid
import pytest
from http import HTTPStatus
from tests.functional.settings import get_settings_instance
from tests.functional.testdata.data_to_elastic import movies
from tests.functional.src.tools import transform_movies_test_data, transform_movies_list_test_data


@pytest.mark.asyncio
async def test_get_film_detailed(create_index, make_get_request):
    out_test_data = transform_movies_test_data(movies[0])
    film_id = out_test_data['uuid']
    response = await make_get_request(f'/films/{film_id}', params={})
    assert response.status == HTTPStatus.OK
    assert response.body['uuid'] == film_id
    assert response.body['title'] == out_test_data['title']
    assert response.body['genre'] == out_test_data['genre']
    assert response.body['actors'] == out_test_data['actors']
    assert response.body['writers'] == out_test_data['writers']
    assert response.body['directors'] == out_test_data['directors']


@pytest.mark.asyncio
async def test_get_all_films(create_index, make_get_request):
    params = {'sort': '-imdb_rating', 'page[number]': 1, 'page[size]': 3}
    response = await make_get_request('/films/', params=params)
    assert response.status == HTTPStatus.OK
    out_test_data = transform_movies_list_test_data(movies)
    sorted_test_data = sorted(out_test_data, key=lambda x: -x['imdb_rating'])
    assert response.body == sorted_test_data[:3]
    assert len(response.body) == 3


@pytest.mark.asyncio
async def test_get_film_unknown(create_index, make_get_request):
    random_uuid = uuid.uuid4()
    response = await make_get_request(f'/films/{random_uuid}')
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == 'film not found'


@pytest.mark.asyncio
async def test_cache_film(create_index, es_client, make_get_request, flush_db):
    random_uuid = uuid.uuid4()

    data = {
        'id': random_uuid,
        'imdb_rating': 7.6,
        'genre': [
            {
                'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                'name': 'Action'
            }
        ],
        'title': 'TestFilm',
        'description': None,
        'directors_names': [],
        'actors_names': [],
        'writers_names': [],
        'actors': [],
        'writers': [],
        'directors': []}

    await es_client.create(
        get_settings_instance().movies_elastic_search_index_name,
        random_uuid,
        data
    )
    response_first = await make_get_request(f'/films/{random_uuid}')
    assert response_first.status == HTTPStatus.OK
    await es_client.delete('movies', random_uuid)
    response_second = await make_get_request(f'/films/{random_uuid}')
    assert response_second.status == HTTPStatus.OK
    assert response_first.body == response_second.body
