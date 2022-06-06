from motor.motor_asyncio import (
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
    AsyncIOMotorClient,
    AsyncIOMotorCursor
)
from bson import ObjectId
from typing import List
from ..client import MongoSession


class BaseAsyncMongoManager:

    COLLECTION_NAME = None

    def __init__(self, mongo_session: MongoSession):
        self._database = mongo_session.database
        self._session = mongo_session.session
        self._client = mongo_session.client

    def get_client(self) -> AsyncIOMotorClient:
        return self._client

    def get_session(self) -> AsyncIOMotorClientSession:
        return self._session

    def get_database(self) -> AsyncIOMotorDatabase:
        return self._database

    def get_collection_name(self) -> str:
        return self.COLLECTION_NAME

    def get_collection(self) -> AsyncIOMotorCollection:
        return self.get_database()[self.get_collection_name()]

    @property
    def db(self) -> AsyncIOMotorDatabase:
        return self.get_database()

    @property
    def session(self) -> AsyncIOMotorClientSession:
        return self.get_session()

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.get_collection()

    @classmethod
    def validate_id(cls, value):
        if isinstance(value, ObjectId):
            return ObjectId
        else:
            return ObjectId(value)

    async def get_object_by_id(self, object_id: ObjectId) -> dict:
        return await self.collection.find_one({"_id": object_id}, session=self.session)

    async def create_object(self, object_data: dict) -> ObjectId:
        return await self.collection.insert_one(object_data, session=self.session)


