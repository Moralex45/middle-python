from __future__ import annotations
import uuid

from motor import motor_asyncio

from src.models.inner.events.like import Like
from src.repositories.like.base import AsyncLikeRepositoryProtocol
import src.core.exceptions.repositories as repositories_exception
import src.core.config as project_config


class AsyncMongoDBLikeRepository(AsyncLikeRepositoryProtocol):
    def __init__(self, mongodb_instance: motor_asyncio.AsyncIOMotorClient):
        database = mongodb_instance[
            project_config.get_settings().mongodb_settings.mongodb_database
        ]
        self.collection: motor_asyncio.AsyncIOMotorCollection = database[
            project_config.get_settings().mongodb_settings.mongodb_likes_collection
        ]

    async def get_movie_likes_amount(self, movie_id: uuid.UUID) -> int:
        query = {'movie_id': str(movie_id)}
        return await self.collection.count_documents(query)

    async def get_average_movie_mark(self, movie_id: uuid.UUID) -> int | None:
        pipeline = [
            {'$match': {'movie_id': f'{str(movie_id)}'}},
            {'$group': {'_id': '$movie_id', 'count': {'$avg': '$mark'}}},
        ]
        aggregation_result = await self.collection.aggregate(pipeline).to_list(1)  # type:ignore
        if len(aggregation_result) != 0:
            return aggregation_result[0]['count']

        return None

    async def create_like(self, user_id: uuid.UUID, movie_id: uuid.UUID, mark: int, device_fingerprint: str) -> Like:
        """
        Raises:
            repositories_exception.DataAlreadyExistsError: on inability to create like

        """
        like = Like(
            _id=uuid.uuid4(), user_id=user_id, movie_id=movie_id, device_fingerprint=device_fingerprint, mark=mark,
        )
        query = {'user_id': str(like.user_id), 'movie_id': str(like.movie_id)}
        if self.collection.find_one(query) is not None:
            raise repositories_exception.DataAlreadyExistsError()
        await self.collection.insert_one(like.to_dict())
        return like

    async def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> None:
        query = {'user_id': str(user_id), 'movie_id': str(movie_id)}
        await self.collection.delete_one(query)
