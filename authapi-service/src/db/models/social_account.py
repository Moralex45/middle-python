from typing import TypeVar

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, UniqueConstraint, String
from src.db.models.base import BaseModel
from src.db.models.users import User

SAT = TypeVar('SAT')


def create_partition(target, connection, **kw) -> None:
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "social_account_yandex" PARTITION OF "social_account" FOR VALUES IN ('yandex')"""
    )


class SocialAccount(BaseModel):

    __tablename__ = "social_account"

    __table_args__ = (
                        UniqueConstraint("social_id", "social_name"),
                        {
                            'postgresql_partition_by': 'LIST (social_name)',
                            'listeners': [('after_create', create_partition)],
                        }
                    )

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)

    social_id = Column(String(length=100), nullable=False)
    social_name = Column(String(length=100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.social_name} {self.user_id}>"
