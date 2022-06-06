import dataclasses

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase
)
from settings import APP_CONFIG
import functools


class CustomAsyncIOMotorClient(AsyncIOMotorClient):

    _counter = 0

    def __init__(
            self,
            host: str,
            port: int,
            username: str,
            password: str,
            database: str,
    ):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self.__class__._counter += 1
        super().__init__(self.get_url())

    def get_url(self) -> str:
        return f"mongodb://{self._username}:{self._password}@{self._host}:{self._port}/{self._database}"

    @classmethod
    def get_count(cls):
        return cls._counter

    def __del__(self):
        self.__class__._counter -= 1


def get_client() -> CustomAsyncIOMotorClient:
    """
    Returns initialized Database Motor client.
    """
    db_client = CustomAsyncIOMotorClient(
        host=APP_CONFIG.MONGO_HOST,
        port=APP_CONFIG.MONGO_PORT,
        username=APP_CONFIG.MONGO_USER,
        password=APP_CONFIG.MONGO_PASSWORD,
        database=APP_CONFIG.MONGO_DATABASE
    )
    return db_client


@dataclasses.dataclass
class MongoSession:
    database: AsyncIOMotorDatabase
    client: AsyncIOMotorClient
    session: AsyncIOMotorClientSession


def with_new_async_mongo_session(
        is_transaction: bool = False
):
    """
    Add mongo_session:MongoSession object to method kwargs.
    And close mongo_session after method complete.
    """
    def wrapper(func):

        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            db_client = get_client()
            async with await db_client.start_session() as session:
                database_session = MongoSession(
                    database=db_client.get_database(APP_CONFIG.MONGO_DATABASE),
                    client=db_client,
                    session=session
                )
                kwargs["mongo_session"] = database_session
                if is_transaction:
                    async with session.start_transaction():
                        result = await func(*args, **kwargs)
                else:
                    result = await func(*args, **kwargs)
                return result
        return wrapped

    return wrapper


