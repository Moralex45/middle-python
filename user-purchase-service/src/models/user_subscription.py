import datetime

from sqlalchemy import (
    Column,
    TIMESTAMP,
    Enum,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base_model import BaseModel
from src.models.addition.addition import PaymentStatus


class UserSubscription(BaseModel):
    __tablename__ = "usubscription"
    __table_args__ = ({'extend_existing': True},)

    user_id = Column(UUID(as_uuid=True))
    payment_id = Column(UUID(as_uuid=True))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.succeed)
    subscription_id = Column(ForeignKey('subscription.id'))

    expiration = Column(DateTime(timezone=True))

    created_at = Column(TIMESTAMP(), default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP(), nullable=True)

    subscription = relationship(
        "Subscription",
        back_populates="usubscription",
        uselist=False, lazy="joined"
    )
