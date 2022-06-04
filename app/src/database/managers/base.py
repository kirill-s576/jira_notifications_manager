from motor.motor_asyncio import AsyncIOMotorClientSession


class BaseAsyncMongoManager:

    def __init__(self, session: AsyncIOMotorClientSession):
        self._session = session

