import logging

from fastapi import APIRouter
from starlette import status

import src.models.http.callback as http_callback

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/v1/callback')


@router.post('/',
             status_code=status.HTTP_200_OK,
             description='Ручка для обработки callback',
             summary='Ручка для обработки callback со стороны биллинг сервиса',
             tags=['Callback'])
async def payment(
    payload: http_callback.CallbackData,
) -> None:
    ...
