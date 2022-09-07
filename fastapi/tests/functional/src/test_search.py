import pytest
from http import HTTPStatus

from tests.functional.testdata.data_to_elastic import movies
from tests.functional.src.tools import transform_movies_list_test_data


@pytest.mark.asyncio
async def test_person_search(create_index, make_get_request):
    params = {'query': 'James', 'page[number]': 1, 'page[size]': 3}
    response = await make_get_request('/persons/search?', params=params)
    assert response.status == HTTPStatus.OK
    assert 'James' in response.body[0]['full_name']


@pytest.mark.asyncio
async def test_film_search(make_get_request):
    params = {'query': 'Star', 'page[number]': 1, 'page[size]': 3}
    response = await make_get_request('/films/search?', params=params)
    assert response.status == HTTPStatus.OK
    assert sorted(response.body, key=lambda x: -x['imdb_rating']) \
           == sorted(transform_movies_list_test_data(movies), key=lambda x: -x['imdb_rating'])
