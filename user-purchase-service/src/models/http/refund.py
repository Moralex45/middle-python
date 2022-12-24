import uuid


from src.models.base import Base


class RefundIN(Base):
    user_id: uuid.UUID | None
    payment_id: uuid.UUID
