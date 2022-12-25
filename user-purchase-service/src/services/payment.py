import datetime
from uuid import UUID
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.sqlalchemy.core import get_session
from src.services.base import BaseService
from src.models.user_subscription import UserSubscription as model_user_subscription
from src.models.user_purchase import UserPurchase as model_user_purchase
from src.models.http.user_purchase import UserPurchase as http_user_purchase_model
import src.models.http.callback as http_callback
from src.models.http.user_subscription import UserSubscription as http_user_subscription_model
from src.models.addition.addition import PaymentStatus
from src.models.http.callback import EventOptions, StatusOptions


class PaymentService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_user_purchase_by_id(self, payment_id: UUID):
        result = await self.session.execute(
            select(model_user_purchase). where(
                model_user_purchase.payment_id == payment_id,
            )
        )
        return result.scalars().first()

    async def get_user_subscription_by_id(self, payment_id: UUID):
        result = await self.session.execute(
            select(model_user_subscription). where(
                model_user_subscription.payment_id == payment_id,
            )
        )
        return result.scalars().first()

    async def create_payment(
        self,
        user_purchase: http_user_purchase_model,
        user_subscription: http_user_subscription_model
    ):
        db_user_purchase = model_user_purchase(**user_purchase.dict())
        self.session.add(db_user_purchase)
        await self.session.commit()
        await self.session.refresh(db_user_purchase)

        db_user_subscription = model_user_subscription(**user_subscription.dict())
        self.session.add(db_user_subscription)
        await self.session.commit()
        await self.session.refresh(db_user_subscription)

        return db_user_purchase, db_user_subscription

    async def update_payment(
        self,
        payload: http_callback.CallbackData,
    ):
        if payload.event.value == EventOptions.payment.value:
            db_user_purchase = await self.get_user_purchase_by_id(
                payload.payment_id
            )
            db_user_subscription = await self.get_user_subscription_by_id(
                payload.sub_payment_id
            )
            if payload.status.value == StatusOptions.canceled.value:

                db_user_purchase.status = payload.status.value
                db_user_subscription.status = payload.status.value

                db_user_purchase.updated_at = datetime.datetime.now()
                db_user_subscription.updated_at = datetime.datetime.now()

                self.session.add(db_user_purchase)
                await self.session.commit()
                await self.session.refresh(db_user_purchase)

                self.session.add(db_user_subscription)
                await self.session.commit()
                await self.session.refresh(db_user_subscription)
        if payload.event.value == EventOptions.rec_payment.value:
            db_user_purchase = await self.get_user_purchase_by_id(
                payload.payment_id
            )
            db_user_subscription = await self.get_user_subscription_by_id(
                payload.sub_payment_id
            )
            if payload.status.value == StatusOptions.canceled.value:
                db_user_purchase.status = PaymentStatus.canseled.value
                db_user_purchase.is_deleted = True

                db_user_subscription.status = PaymentStatus.canseled.value

                db_user_purchase.updated_at = datetime.datetime.now()
                db_user_subscription.updated_at = datetime.datetime.now()

                self.session.add(db_user_purchase)
                await self.session.commit()
                await self.session.refresh(db_user_purchase)

                self.session.add(db_user_subscription)
                await self.session.commit()
                await self.session.refresh(db_user_subscription)
            else:
                db_user_subscription.status = PaymentStatus.succeeded.value
                db_user_subscription.updated_at = datetime.datetime.now()
                self.session.add(db_user_subscription)
                await self.session.commit()
                await self.session.refresh(db_user_subscription)
        if payload.event.value == EventOptions.refund.value:
            await self.payment_refund(payload.payment_id, payload.sub_payment_id)

    async def payment_refund(self, payment_id: UUID, sub_payment_id: UUID):
        db_user_purchase = await self.get_user_purchase_by_id(payment_id)
        db_user_subscription = await self.get_user_subscription_by_id(sub_payment_id)
        db_user_purchase.status = PaymentStatus.refunded.value
        db_user_purchase.is_deleted = True
        db_user_purchase.updated_at = datetime.datetime.now()

        self.session.add(db_user_purchase)
        await self.session.commit()
        await self.session.refresh(db_user_purchase)

        db_user_subscription.status = PaymentStatus.refunded.value
        db_user_subscription.updated_at = datetime.datetime.now()

        self.session.add(db_user_subscription)
        await self.session.commit()
        await self.session.refresh(db_user_subscription)

        return PaymentStatus.refunded.value


@lru_cache()
def get_payment_service(
    session: AsyncSession = Depends(get_session)
) -> PaymentService:
    return PaymentService(session)
