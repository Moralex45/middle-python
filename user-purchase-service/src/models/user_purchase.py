import datetime

from sqlalchemy import (
    Column,
    TIMESTAMP,
    Enum,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from src.models.base_model import BaseModel
from src.models.addition.addition import PaymentStatus, ProductType


class UserPurchase(BaseModel):
    __tablename__ = "upurchase"
    __table_args__ = ({'extend_existing': True},)

    user_id = Column(UUID(as_uuid=True))
    product_type = Column(Enum(ProductType))
    product_id = Column(UUID(as_uuid=True))
    payment_id = Column(UUID(as_uuid=True))

    status = Column(Enum(PaymentStatus))

    is_deleted = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP(), nullable=True)
