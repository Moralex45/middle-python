import typing
import uuid

from motor import motor_asyncio

import src.models.user_activities as user_act
import src.utils.exceptions as exc


class LikesRepositoryProtocol(typing.Protocol):

    async def get_user_id_by_review(self, review_id: uuid.UUID) -> user_act.Review:
        ...


class LikesMongoRepository(LikesRepositoryProtocol):

    def __init__(self,
                 mongo_client: motor_asyncio.AsyncIOMotorClient,
                 *,
                 database_name: str,
                 collection_name: str):
        database = mongo_client[database_name]
        self.__collection: motor_asyncio.AsyncIOMotorCollection = database[collection_name]

    async def get_user_id_by_review(self, review_id: uuid.UUID) -> user_act.Review:
        query = {'_id': str(review_id)}
        document: dict | None = await self.__collection.find_one(query)  # type:ignore
        if document is None:
            raise exc.NotFoundError
        return user_act.Review(**document)
