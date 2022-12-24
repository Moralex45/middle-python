import typing
import uuid
from functools import lru_cache

import aiohttp

from src.core.config import get_settings_instance
from src.utils.backoff import Backoff
from src.models.internal.billing_service import (PaymentCreate, RecurrentPaymentUpdate,
                                                 PaymentCreateResponse, BillingServiceUrls)


class ServiceNotAvailableError(Exception):
    ...


class BillingServiceProtocol(typing.Protocol):

    async def create_payment(
            self,
            payment: PaymentCreate,
    ) -> str:
        """
        :return str: return redirect url
        :raises ServiceNotAvailableError: is service has fallen
        """
        ...

    async def update_recurrent_payment(
            self,
            sub_payment_id: uuid.UUID,
            update_rec_payment: RecurrentPaymentUpdate,
    ) -> None:
        """
        :raises ServiceNotAvailableError: is service has fallen
        """
        ...

    async def refund_payment(
            self,
            payment_id: uuid.UUID,
            amount: float,
    ) -> None:
        """
        :raises ServiceNotAvailableError: is service has fallen
        """
        ...

    async def dispose(self) -> None:
        ...


class BillingService(BillingServiceProtocol):

    def __init__(
            self,
            service_url: str,
    ) -> None:
        self.__session = aiohttp.ClientSession(service_url)

    @Backoff(exception=ServiceNotAvailableError)
    async def create_payment(
            self,
            payment: PaymentCreate,
    ) -> str:
        body = payment.dict(exclude_none=True)
        async with self.__session.post(BillingServiceUrls.create_payment.value, json=body) as response:
            if response.status >= 500:
                raise ServiceNotAvailableError
            redirect_url = PaymentCreateResponse.parse_obj(response.json()).redirect_url
        return redirect_url

    @Backoff(exception=ServiceNotAvailableError)
    async def update_recurrent_payment(
            self,
            sub_payment_id: uuid.UUID,
            update_rec_payment: RecurrentPaymentUpdate,
    ) -> None:
        body = update_rec_payment.dict(exclude_none=True)
        url = BillingServiceUrls.update_rec_payment.value % sub_payment_id
        async with self.__session.post(url, json=body) as response:
            if response.status >= 500:
                raise ServiceNotAvailableError

    @Backoff(exception=ServiceNotAvailableError)
    async def refund_payment(
            self,
            payment_id: uuid.UUID,
            amount: float,
    ) -> None:
        body = {'amount': amount}
        url = BillingServiceUrls.refund_payment.value % payment_id
        async with self.__session.post(url, json=body) as response:
            if response.status >= 500:
                raise ServiceNotAvailableError

    async def dispose(self) -> None:
        await self.__session.close()


@lru_cache()
def get_billing_service_instance() -> BillingServiceProtocol:
    return BillingService(
        get_settings_instance().BILLING_SERVICE_URL,
    )
