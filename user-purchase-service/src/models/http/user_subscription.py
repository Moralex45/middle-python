import uuid
from datetime import date

from src.models.base import Base


class UserSubscription(Base):
    user_id: uuid.UUID
    payment_id: uuid.UUID
    subscription_id: uuid.UUID
    expiration: date
