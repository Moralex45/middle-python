import fastapi

import src.core.utils as endpoints_utils
import src.models.http.events as events_http_models
import src.models.inner.events as events_inner_models
import src.repositories.events as events_repository

router = fastapi.APIRouter(prefix='/api/v1/events')


@router.post(
    '/movie_watching',
    dependencies=[fastapi.Depends(endpoints_utils.verify_auth_tokens)],
)
async def film_search(
        movie_watching_event_request_model: events_http_models.MovieWatchingEventRequestBody,
        events_repository_instance: events_repository.EventRepositoryProtocol = fastapi.Depends(events_repository.get_event_repository)  # noqa
):
    movie_watching_event: events_inner_models.MovieWatchingEvent = events_inner_models.MovieWatchingEvent(
        **movie_watching_event_request_model.dict()
    )
    await events_repository_instance.produce(movie_watching_event)
