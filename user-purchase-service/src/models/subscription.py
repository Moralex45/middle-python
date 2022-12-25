from sqlalchemy import (
    Column,
    INT,
    TEXT
)
from sqlalchemy.orm import relationship
from src.models.base_model import BaseModel


class Subscription(BaseModel):
    __tablename__ = "subscription"
    __table_args__ = ({'extend_existing': True},)

    description = Column(TEXT(), default='')
    price = Column(INT(), nullable=False)
    duration = Column(INT(), nullable=False)

    usubscription = relationship("UserSubscription", back_populates="subscription")
