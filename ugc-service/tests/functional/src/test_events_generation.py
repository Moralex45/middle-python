import http

import orjson
import pytest

from tests.functional.testdata.events import events
import src.models.http.events as http_events_models
import src.models.inner.events as inner_events_models


@pytest.mark.parametrize(
    'event',
    [event for event in events]
)
@pytest.mark.asyncio
async def test_simple_generation(get_web_test_client, get_kafka_client, event):
    request_event_model = http_events_models.MovieWatchingEventRequestBody(**event)
    request_event_dict = request_event_model.dict()
    request_event_dict['movie_id'] = str(request_event_dict['movie_id'])
    request_event_dict['user_id'] = str(request_event_dict['user_id'])

    response = get_web_test_client.post('/api/v1/events/movie_watching', json=request_event_dict)
    assert response.status_code == http.HTTPStatus.OK

    kafka_record = await get_kafka_client.getone()
    kafka_record_key = kafka_record.key.decode()
    event_model = inner_events_models.MovieWatchingEvent(**orjson.loads(kafka_record.value.decode()))

    assert kafka_record_key == f'{event_model.user_id}+{event_model.movie_id}'
    assert event_model.dict() == request_event_model.dict()
