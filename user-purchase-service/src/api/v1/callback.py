import logging
from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from starlette import status

from src.services.payment import PaymentService, get_payment_service
import src.models.http.callback as http_callback
from src.api.errors import errors_description

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/v1/callback')


@router.post('/',
             status_code=status.HTTP_200_OK,
             description='Ручка для обработки callback',
             summary='Ручка для обработки callback со стороны биллинг сервиса',
             tags=['Callback'])
async def payment(
    payload: http_callback.CallbackData,
    payment_service: PaymentService = Depends(get_payment_service)
) -> None:
    db_payment = await payment_service.get_user_purchase_by_id(
        payload.payment_id
    )
    if not db_payment:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=errors_description.no_payment
        )

    await payment_service.update_payment(
        payload
    )
