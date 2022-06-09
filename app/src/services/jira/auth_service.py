from src.utils.jira_async_api import (
    JiraOAuthAsyncApi,
    JiraAsyncApi
)
from settings import APP_CONFIG
from src.database.models.jira_account import (
    JiraToken,
    JiraAccountCreate
)
from src.database.client import (
    with_new_async_mongo_session,
    MongoSession
)
from src.database.managers.jira_account import JiraAccountAsyncMongoManager
from src.database.managers.user import UserAsyncMongoManager
from src.database.models.user import UserReadModel
from typing import Optional


class JiraAuthAsyncService:

    def __init__(self):
        self.jira_auth_api = JiraOAuthAsyncApi(
            client_id=APP_CONFIG.JIRA_APP_CLIENT_ID,
            client_secret=APP_CONFIG.JIRA_APP_SECRET,
            redirect_uri=f"https://{APP_CONFIG.SERVER_HOST}/jira_auth/confirm_oauth",
            scope=APP_CONFIG.JIRA_AUTH_SCOPE_LIST
        )

    @with_new_async_mongo_session()
    async def _get_db_user_by_state(self, user_state: str, mongo_session: MongoSession) -> Optional[UserReadModel]:
        user_manager = UserAsyncMongoManager(mongo_session)
        user = await user_manager.get_user_by_telegram_chat_id(chat_id=user_state)
        return user

    @with_new_async_mongo_session()
    async def save_accessible_resource(
        self,
        user_id: str,
        token: JiraToken,
        resource: dict,
        mongo_session: MongoSession = None
    ):
        jira_account = self.__get_account_model(user_id, token, resource)
        jira_account_manager = JiraAccountAsyncMongoManager(mongo_session)
        await jira_account_manager.get_and_replace_or_create_account(jira_account)

    async def confirm_oauth(self, code: str, user_state: str, mongo_session: MongoSession = None):
        """
        Creates new account and returns redirect url.
        """
        auth_token_data = await self.jira_auth_api.exchange_code_to_jwt(code)
        token_object = self.__get_token_model(auth_token_data)
        jira_api = JiraAsyncApi(token_object.access_token, token_object.refresh_token)
        accessible_resources = await jira_api.get_accessible_resources()
        user: UserReadModel = await self._get_db_user_by_state(user_state)
        for resource in accessible_resources:
            await self.save_accessible_resource(
                user_id=user.id,
                token=token_object,
                resource=resource
            )
            # TODO: Subscribe for getting notifications via Webhook
        return self._get_after_auth_redirect_uri()

    def _get_auth_uri(self, user_state: str) -> str:
        return self.jira_auth_api.get_auth_uri(user_state=user_state)

    @staticmethod
    def _get_after_auth_redirect_uri():
        return f"tg://resolve?domain={APP_CONFIG.TELEGRAM_BOT_NAME}"

    @staticmethod
    def __get_account_model(user_id: str, token: JiraToken, resource: dict):
        jira_account = JiraAccountCreate(
            user_id=user_id,
            token=token,
            resource_id=resource["id"],
            resource_name=resource["name"],
            scopes=resource["scopes"],
            resource_url=resource["url"],
            avatar_url=resource["avatarUrl"],
        )
        return jira_account

    @staticmethod
    def __get_token_model(token_data: dict) -> JiraToken:
        token_model = JiraToken(**token_data)
        return token_model


class JiraResourceService:

    def __init__(self, access_token: str, resource_id: str):
        pass


