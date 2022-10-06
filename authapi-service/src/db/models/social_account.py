from typing import TypeVar

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, UniqueConstraint, String
from src.db.models.base import BaseModel
from src.db.models.users import User

from src.db.core import db_session

SAT = TypeVar('SAT')

class SocialAccount(BaseModel):

    __tablename__ = "social_account"

    __table_args__ = (UniqueConstraint("social_id", "social_name"),
                      {'extend_existing': True},)

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)

    social_id = Column(String(length=100), nullable=False)
    social_name = Column(String(length=100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.social_name} {self.user_id}>"

    def save_to_db(self) -> None:
        with db_session() as session:
            session.add(self)
            session.commit()

    @classmethod
    def raw_exists(cls, user_id: str, social_id: str, social_name: str):
        return cls.query.filter_by(
            user_id=user_id, social_id=social_id, social_name=social_name
        ).first()
