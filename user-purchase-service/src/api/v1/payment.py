import logging
from http import HTTPStatus
from datetime import timedelta, date

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)

from src.services.payment import PaymentService, get_payment_service
from src.services.subscription import SubscriptionService, get_subscription_service
from src.models.http.user_purchase import UserPurchase as http_user_purchase_model
from src.models.http.user_purchase import UserPurchaseIN as http_user_purchasein_model
from src.models.http.user_subscription import UserSubscription as http_user_subscription_model
from src.api.errors import errors_description

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/v1/payment')


@router.post('/',
             response_model=http_user_subscription_model,
             status_code=status.HTTP_201_CREATED,
             description='Ручка для совершения оплаты',
             summary='Ручка для совершения оплаты для конкретного продукта(фильма, подписки)',
             tags=['Платежи'])
async def payment(
    user_purchase: http_user_purchasein_model,
    payment_service: PaymentService = Depends(get_payment_service),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    db_subscription = await subscription_service.get_subscription_by_id(user_purchase.subscription_id)
    if not db_subscription:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors_description.subscription_not_found
        )
    db_user_purchase = await payment_service.get_user_purchase_by_id(
            user_id=user_purchase.user_id,
            payment_id=user_purchase.payment_id
        )
    if db_user_purchase:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=errors_description.purchase_already_exists
        )
    db_user_subscription = await payment_service.get_user_subscription_by_id(
            payment_id=user_purchase.payment_id
        )
    if db_user_subscription:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=errors_description.user_has_this_subscription
        )

    new_user_purchase = http_user_purchase_model(
        user_id=user_purchase.user_id,
        product_type=user_purchase.product_type,
        product_id=user_purchase.product_id,
        payment_id=user_purchase.payment_id,
    )

    new_db_user_subscription = http_user_subscription_model(
        user_id=user_purchase.user_id,
        payment_id=user_purchase.payment_id,
        subscription_id=user_purchase.subscription_id,
        expiration=date.today() + timedelta(days=db_subscription.duration)
    )

    await payment_service.create_payment(
                                            new_user_purchase,
                                            new_db_user_subscription
                                        )
    return new_db_user_subscription
