import uuid

from sqlalchemy.exc import IntegrityError

from src.db.core import db_session
from src.db.models.social_account import SAT, SocialAccount
from src.db.services.base import ISocialAccountService


class SocialAccountService(ISocialAccountService):
    @classmethod
    def get_by_id(cls, _id: uuid.UUID) -> SocialAccount | None:
        with db_session() as session:
            return session.query(SocialAccount).filter_by(id=_id).first()

    @classmethod
    def create(
        cls,
        user_id: uuid.UUID,
        social_id: str,
        social_name: str
    ) -> SAT:
        with db_session() as session:
            db_social_account = SocialAccount(
                user_id=user_id,
                social_id=social_id,
                social_name=social_name
            )

            session.add(db_social_account)

            try:
                session.commit()

            except IntegrityError:
                raise ValueError('Unable to create social-account with passed parameters. '
                                 'Instance already exists')

            return cls.get_by_id(db_social_account.id)

    @classmethod
    def get_filtered_by_user_id_and_social_id_and_social_name(
        cls,
        user_id: uuid.UUID,
        social_id: str,
        social_name: str
    ) -> SAT | None:
        with db_session() as session:
            return session.query(SocialAccount).filter_by(
                user_id=user_id,
                social_id=social_id,
                social_name=social_name
            ).first()
