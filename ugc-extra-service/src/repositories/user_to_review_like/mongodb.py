from __future__ import annotations

import uuid

from motor import motor_asyncio

import src.core.config as project_config
import src.core.exceptions.repositories as repositories_exception
from src.models.inner.events.user_to_review_like import UserToReviewLike
from src.repositories.user_to_review_like.base import AsyncUserToReviewLikeRepositoryProtocol


class AsyncMongoDBUserToReviewLikeRepository(AsyncUserToReviewLikeRepositoryProtocol):
    def __init__(self, mongodb_instance: motor_asyncio.AsyncIOMotorClient):
        database = mongodb_instance[
            project_config.get_settings().mongodb_settings.mongodb_database
        ]
        self.collection: motor_asyncio.AsyncIOMotorCollection = database[
            project_config.get_settings().mongodb_settings.mongodb_users_to_reviews_likes_collection
        ]

    async def create_like(
            self, user_id: uuid.UUID, review_id: uuid.UUID, mark: int, _id: uuid.UUID | None = None,
    ) -> UserToReviewLike:
        """
        Raises:
            repositories_exception.DataAlreadyExistsError: on inability to create user_to_film_like

        """
        like = UserToReviewLike(
            _id=uuid.uuid4() if _id is None else _id,
            user_id=user_id,
            review_id=review_id,
            mark=mark,
        )
        if await self.get_like(like.user_id, like.review_id) is not None:
            raise repositories_exception.DataAlreadyExistsError()
        await self.collection.insert_one(like.to_dict())
        return like

    async def delete_like(self, user_id: uuid.UUID, review_id: uuid.UUID) -> None:
        """
        Raises:
            repositories_exception.DataDoesNotExistError: on inability to delete user_to_film_like

        """
        if await self.get_like(user_id, review_id) is None:
            raise repositories_exception.DataDoesNotExistError()
        query = {'user_id': str(user_id), 'review_id': str(review_id)}
        await self.collection.delete_one(query)

    async def get_like(self, user_id: uuid.UUID, review_id: uuid.UUID) -> UserToReviewLike | None:
        query = {'user_id': str(user_id), 'review_id': str(review_id)}
        document: dict | None = await self.collection.find_one(query)  # type:ignore
        if document is not None:
            return UserToReviewLike(**document)

        return None

    async def get_average_review_mark(self, review_id: uuid.UUID) -> float | None:
        pipeline = [
            {'$match': {'review_id': f'{str(review_id)}'}},
            {'$group': {'_id': '$review_id', 'count': {'$avg': '$mark'}}},
        ]
        aggregation_result = await self.collection.aggregate(pipeline).to_list(1)  # type:ignore
        if len(aggregation_result) != 0:
            return aggregation_result[0]['count']

        return None
