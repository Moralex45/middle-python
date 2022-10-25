from fastapi import APIRouter, Depends

from src.core.utils import verify_auth_tokens
from src.models.http.events import MovieWatchingEventRequestBody
from src.services.events import get_event_service, EventService

router = APIRouter(prefix='/api/v1/events')


@router.post(
    '/movie_watching',
    dependencies=[Depends(verify_auth_tokens)],
)
async def film_search(movie_watching_event: MovieWatchingEventRequestBody,
                      events_service: EventService = Depends(get_event_service)):
    await events_service.produce_movie_watching(movie_watching_event)
