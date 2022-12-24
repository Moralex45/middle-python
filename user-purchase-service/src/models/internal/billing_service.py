import enum
import uuid

from src.models.base import Base


class PaymentCreate(Base):
    id: uuid.UUID  # noqa: VNE003
    user_id: uuid.UUID
    value: float
    description: str
    recurrent: bool | None = False
    recurrent_period: int | None


class PaymentCreateResponse(Base):
    redirect_url: str


class RecurrentPaymentUpdate(Base):

    amount: float | None
    is_active: bool | None


class BillingServiceUrls(enum.Enum):
    create_payment = '/api/v1/payment/'
    refund_payment = '/api/v1/payment/%s/refund'
    update_rec_payment = '/api/v1/rec_payment/%s'
