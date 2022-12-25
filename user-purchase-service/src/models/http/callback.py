import enum
import uuid

from src.models.base import Base


class EventOptions(enum.Enum):
    payment = 'payment'
    rec_payment = 'rec_payment'
    refund = 'refund'


class StatusOptions(enum.Enum):
    succeeded = 'succeeded'
    canceled = 'canceled'
    refunded = 'refunded'


class CallbackData(Base):
    event: EventOptions
    payment_id: uuid.UUID
    status: StatusOptions
    sub_payment_id: uuid.UUID | None
