import typing
import uuid

from motor import motor_asyncio

import src.models.user_activities as user_act
import src.utils.exceptions as exc


class ReviewRepositoryProtocol(typing.Protocol):

    async def get_review_by_id(self, review_id: uuid.UUID) -> user_act.Review:
        """
        :raises NotFoundError:
        """
        ...


class ReviewMongoRepository(ReviewRepositoryProtocol):

    def __init__(self,
                 mongo_client: motor_asyncio.AsyncIOMotorClient,
                 *,
                 database_name: str,
                 collection_name: str):
        database = mongo_client[database_name]
        self._collection: motor_asyncio.AsyncIOMotorCollection = database[collection_name]

    async def get_review_by_id(self, review_id: uuid.UUID) -> user_act.Review:
        query = {'_id': str(review_id)}
        document: dict | None = await self._collection.find_one(query)  # type:ignore
        if document is None:
            raise exc.NotFoundError
        return user_act.Review(**document)
