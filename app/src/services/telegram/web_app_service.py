from typing import List
import hmac
import hashlib
from urllib.parse import unquote, parse_qsl, urlsplit
import json
from pydantic import BaseModel
import datetime
from src.database.models.jira_account import JiraAccountRead
from src.database.client import with_new_async_mongo_session, MongoSession
from src.database.managers.jira_account import JiraAccountAsyncMongoManager
from src.database.managers.user import UserAsyncMongoManager


class WebAppUser(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    language_code: str


class SafeWebAppInitData(BaseModel):
    query_id: str
    user: WebAppUser
    auth_date: datetime.datetime


class InvalidWebAppInitDataError(Exception):
    pass


class TelegramCheckString:

    def __init__(self, check_string: str, bot_token: str):
        self.original_check_string = check_string
        self.bot_token = bot_token

    @property
    def check_dict(self) -> dict:
        unquoted_check_string = unquote(self.original_check_string)
        check_dict = dict(parse_qsl(urlsplit("?" + unquoted_check_string).query))
        return check_dict

    @property
    def safe_init_data_object(self) -> SafeWebAppInitData:
        dct = self.check_dict
        dct["user"] = json.loads(dct["user"])
        return SafeWebAppInitData(**dct)

    @property
    def check_array(self) -> list:
        arr = [f"{key}={value}" for key, value in self.check_dict.items() if key != "hash"]
        arr.sort()
        return arr

    @property
    def final_check_string(self):
        final_check_string = "\n".join(self.check_array)
        return final_check_string

    @property
    def secret_key(self):
        secret_key = hmac.new("WebAppData".encode(), self.bot_token.encode(), hashlib.sha256).digest()
        return secret_key

    @property
    def calculated_hash(self):
        calculated_hash = hmac.new(self.secret_key, self.final_check_string.encode(), hashlib.sha256).hexdigest()
        return calculated_hash

    @property
    def received_hash(self) -> str:
        return self.check_dict["hash"]

    def verify(self) -> bool:
        try:
            return self.calculated_hash == self.received_hash
        except KeyError:
            raise InvalidWebAppInitDataError("Init data has incorrect format")


class WebAppAsyncService:

    def __init__(self, init_data: str, bot_token: str):
        """
        Check-string is the initData, received from Telegram WebApp.
        """
        self._init_data = init_data
        self._bot_token = bot_token

    @property
    def verified_init_data(self) -> TelegramCheckString:
        chs = TelegramCheckString(
            self._init_data,
            self._bot_token
        )
        if not chs.verify():
            raise Exception("Unverified WebApp data")
        return chs

    @with_new_async_mongo_session()
    async def get_jira_accounts(self, mongo_session: MongoSession = None) -> List[JiraAccountRead]:
        user_id = self.verified_init_data.safe_init_data_object.user.id
        user_manager = UserAsyncMongoManager(mongo_session)
        user = await user_manager.get_user_by_telegram_chat_id(str(user_id))
        db_manager = JiraAccountAsyncMongoManager(mongo_session)
        accounts = await db_manager.get_user_accounts(user_id=str(user.id))
        return accounts
