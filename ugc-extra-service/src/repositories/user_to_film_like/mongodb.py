from __future__ import annotations

import uuid

from motor import motor_asyncio

import src.core.config as project_config
import src.core.exceptions.repositories as repositories_exception
from src.models.inner.events.user_to_film_like import UserToFilmLike
from src.repositories.user_to_film_like.base import \
    AsyncUserToFilmLikeRepositoryProtocol


class AsyncMongoDBUserToFilmLikeRepository(AsyncUserToFilmLikeRepositoryProtocol):
    def __init__(self, mongodb_instance: motor_asyncio.AsyncIOMotorClient):
        database = mongodb_instance[
            project_config.get_settings().mongodb_settings.mongodb_database
        ]
        self.collection: motor_asyncio.AsyncIOMotorCollection = database[
            project_config.get_settings().mongodb_settings.mongodb_users_to_films_likes_collection
        ]

    async def get_movie_likes_amount(self, movie_id: uuid.UUID) -> int:
        query = {'movie_id': str(movie_id)}

        return await self.collection.count_documents(query)

    async def get_average_movie_mark(self, movie_id: uuid.UUID) -> float | None:
        pipeline = [
            {'$match': {'movie_id': f'{str(movie_id)}'}},
            {'$group': {'_id': '$movie_id', 'count': {'$avg': '$mark'}}},
        ]
        aggregation_result = await self.collection.aggregate(pipeline).to_list(1)  # type:ignore
        if len(aggregation_result) != 0:
            return aggregation_result[0]['count']

        return None

    async def create_like(
            self, user_id: uuid.UUID, movie_id: uuid.UUID, mark: int, _id: uuid.UUID | None = None,
    ) -> UserToFilmLike:
        """
        Raises:
            repositories_exception.DataAlreadyExistsError: on inability to create user_to_film_like

        """
        like = UserToFilmLike(
            _id=uuid.uuid4() if _id is None else _id,
            user_id=user_id,
            movie_id=movie_id,
            mark=mark,
        )
        if await self.get_like(like.user_id, like.movie_id) is not None:
            raise repositories_exception.DataAlreadyExistsError()
        await self.collection.insert_one(like.to_dict())

        return like

    async def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> None:
        """
        Raises:
            repositories_exception.DataDoesNotExistError: on inability to delete user_to_film_like

        """
        if await self.get_like(user_id, movie_id) is None:
            raise repositories_exception.DataDoesNotExistError()
        query = {'user_id': str(user_id), 'movie_id': str(movie_id)}

        await self.collection.delete_one(query)

    async def get_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> UserToFilmLike | None:
        query = {'user_id': str(user_id), 'movie_id': str(movie_id)}
        document: dict | None = await self.collection.find_one(query)  # type:ignore
        if document is not None:
            return UserToFilmLike(**document)

        return None
