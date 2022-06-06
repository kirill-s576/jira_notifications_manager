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


class JiraAuthAsyncService:

    def __init__(self):
        self.jira_auth_api = JiraOAuthAsyncApi(
            client_id=APP_CONFIG.JIRA_APP_CLIENT_ID,
            client_secret=APP_CONFIG.JIRA_APP_SECRET,
            redirect_uri=f"https://{APP_CONFIG.SERVER_HOST}/jira_auth/confirm_oauth",
            scope=APP_CONFIG.JIRA_AUTH_SCOPE_LIST
        )

    def get_auth_uri(self, user_state: str) -> str:
        return self.jira_auth_api.get_auth_uri(user_state=user_state)

    @staticmethod
    def get_account_model(user_id: str, token: JiraToken, resource: dict):
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

    @with_new_async_mongo_session()
    async def confirm_oauth(self, code: str, user_state: str, mongo_session: MongoSession):
        """
        Creates new account and returns redirect url.
        """
        auth_token_data = await self.jira_auth_api.exchange_code_to_jwt(code)
        token_object = JiraToken(**auth_token_data)
        jira_api = JiraAsyncApi(token_object.access_token, token_object.refresh_token)
        accessible_resources = await jira_api.get_accessible_resources()
        resource = accessible_resources[0]
        jira_account = self.get_account_model(user_state, token_object, resource)
        jira_account_manager = JiraAccountAsyncMongoManager(mongo_session)
        await jira_account_manager.get_and_replace_or_create_account(jira_account)
        return f"tg://resolve?domain={APP_CONFIG.TELEGRAM_BOT_NAME}"
