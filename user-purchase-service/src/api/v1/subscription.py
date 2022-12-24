from uuid import UUID
import logging
from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.exc import IntegrityError

from src.models.http.subscription import Subscription as http_subscription_model
from src.models.http.subscription import SubscriptionPUT as http_subscriptionput_model
from src.services.subscription import SubscriptionService, get_subscription_service
from src.api.errors import errors_description

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/api/v1/subscription')


@router.post('/',
             response_model=http_subscription_model,
             status_code=status.HTTP_201_CREATED,
             description='Ручка для создания подписок',
             summary='Ручка для создания конкретных подписок',
             tags=['Подписки'])
async def create_subscription(
    subscription: http_subscription_model,
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    try:
        await subscription_service.create_subscription(subscription=subscription)
        return subscription
    except IntegrityError as e:
        logger.error(e)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=errors_description.duplication_subscription
        )


@router.put('/{subscription_id}',
            response_model=http_subscriptionput_model,
            status_code=status.HTTP_201_CREATED,
            description='Ручка для обновления подписки',
            summary='Обновление данных подписки в соответствии с моделью',
            tags=['Подписки'])
async def update_subscription(
    subscription_id: UUID,
    subscription: http_subscriptionput_model,
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    db_subscription = await subscription_service.get_subscription_by_id(subscription_id)
    if not db_subscription:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors_description.subscription_not_found
        )
    result = await subscription_service.update_subscription(
            subscription=subscription,
            subscription_id=subscription_id
        )
    response_result = http_subscription_model(
        description=result.description,
        price=result.price,
        duration=result.duration,
    )
    return response_result
