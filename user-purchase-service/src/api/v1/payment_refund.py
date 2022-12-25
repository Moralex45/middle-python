from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi.responses import JSONResponse

from src.services.payment import PaymentService, get_payment_service
from src.models.http.refund import RefundIN as http_refund_model
from src.api.errors import errors_description

router = APIRouter(prefix='/api/v1/payment_ref')


@router.put('/',
            description='Ручка для возврата платежа',
            summary='Ручка для возврата платежа для конкретного продукта(фильма, подписки)',
            tags=['Платежи'])
async def payment(
    refund: http_refund_model,
    payment_service: PaymentService = Depends(get_payment_service)
):
    db_payment = await payment_service.get_user_purchase_by_id(
        user_id=refund.user_id,
        payment_id=refund.payment_id
    )
    if not db_payment:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=errors_description.no_payment
        )

    await payment_service.payment_refund(
        refund.payment_id,
        refund.sub_payment_id
    )

    return JSONResponse(
        content='OK',
        status_code=HTTPStatus.OK
    )
