from __future__ import annotations

import datetime
import uuid

from motor import motor_asyncio

import src.core.config as project_config
import src.core.exceptions.repositories as repositories_exception
from src.models.inner.events.review import Review
from src.repositories.review.base import ReviewRepositoryProtocol


class AsyncMongoDBReviewRepository(ReviewRepositoryProtocol):
    def __init__(
            self,
            mongodb_instance: motor_asyncio.AsyncIOMotorClient,
    ):
        database = mongodb_instance[
            project_config.get_settings().mongodb_settings.mongodb_database
        ]
        self.collection: motor_asyncio.AsyncIOMotorCollection = database[
            project_config.get_settings().mongodb_settings.mongodb_reviews_collection
        ]

    async def create_review(
            self, user_id: uuid.UUID, movie_id: uuid.UUID, review_text: str, _id: uuid.UUID | None = None) -> Review:
        """
        Raises:
            repositories_exception.DataAlreadyExistsError: on inability to create review

        """
        review = Review(
            _id=uuid.uuid4() if _id is None else _id,
            user_id=user_id,
            movie_id=movie_id,
            text=review_text,
            publication_timestamp=datetime.datetime.now().timestamp(),
        )
        if await self.get_review(review.id) is not None or \
                await self.get_review_by_user_id_and_movie_id(user_id, movie_id) is not None:
            raise repositories_exception.DataAlreadyExistsError()
        await self.collection.insert_one(review.to_dict())
        return review

    async def get_review_by_user_id_and_movie_id(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> Review | None:
        query = {'user_id': str(user_id), 'movie_id': str(movie_id)}
        document: dict | None = await self.collection.find_one(query)  # type:ignore
        if document is not None:
            return Review(**document)

        return None

    async def get_review(self, review_id: uuid.UUID) -> Review | None:
        query = {'review_id': str(review_id)}
        document: dict | None = await self.collection.find_one(query)  # type:ignore
        if document is not None:
            return Review(**document)

        return None

    async def get_reviews_by_user_id(self, user_id: uuid.UUID) -> list[Review]:
        query = {'user_id': str(user_id)}
        documents = await self.collection.find(query).to_list(await self.__count_documents(query))
        return [Review(**document) for document in documents]

    async def get_reviews_by_movie_id(self, movie_id: uuid.UUID) -> list[Review]:
        query = {'movie_id': str(movie_id)}
        documents = await self.collection.find(query).to_list(await self.__count_documents(query))
        return [Review(**document) for document in documents]

    async def __count_documents(self, query: dict) -> int:
        return await self.collection.count_documents(query)
