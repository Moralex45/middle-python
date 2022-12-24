from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.sqlalchemy.core import get_session
from src.services.base import BaseService
from src.models.subscription import Subscription as model_subscription
from src.models.http.subscription import Subscription as http_subscription_model


class SubscriptionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_subscription(self, subscription: http_subscription_model):
        db_subscription = model_subscription(**subscription.dict())
        self.session.add(db_subscription)
        await self.session.commit()
        await self.session.refresh(db_subscription)
        return db_subscription

    async def get_subscription_by_id(self, subscription_id):
        result = await self.session.execute(
            select(model_subscription).where(model_subscription.id == subscription_id)
        )
        return result.scalars().first()

    async def update_subscription(
        self,
        subscription: http_subscription_model,
        subscription_id: UUID
    ):
        db_subscription = await self.get_subscription_by_id(subscription_id)
        if subscription.description:
            db_subscription.description = subscription.description
        if subscription.price:
            db_subscription.price = subscription.price
        if subscription.duration:
            db_subscription.duration = subscription.duration
        self.session.add(db_subscription)
        await self.session.commit()
        await self.session.refresh(db_subscription)
        return db_subscription


@lru_cache()
def get_subscription_service(
        session: AsyncSession = Depends(get_session)
) -> SubscriptionService:
    return SubscriptionService(session)
