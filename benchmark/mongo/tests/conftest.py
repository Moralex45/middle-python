import asyncio
from uuid import uuid4

import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient


@pytest_asyncio.fixture(scope="session")
def users_list():
    return [str(uuid4()) for _ in range(100000)]


@pytest_asyncio.fixture(scope="session")
def movies_list():
    return [str(uuid4()) for _ in range(100000)]


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def mongo_db():
    client = AsyncIOMotorClient('localhost', 27019)
    db = client['UGC_data']
    yield db


@pytest_asyncio.fixture(scope="session")
async def get_random_user_id(mongo_db):
    cursor = mongo_db['bookmarks'].aggregate(
        [
            {"$limit": 1000},
            {"$sample": {"size": 1}}
        ]
    )
    document = await cursor.to_list(length=1)
    return document[0]["user_id"]


@pytest_asyncio.fixture(scope="session")
async def get_random_movie_id(mongo_db):
    cursor = mongo_db['likes'].aggregate(
        [
            {"$match": {"movie_id": {"$exists": "true"}}},
            {"$sample": {"size": 1}}
        ]
    )
    document = await cursor.to_list(length=1)
    return document[0]["movie_id"]
