from pydantic import BaseSettings
from typing import List
from src.utils.message_bus import AsyncMessageBus


class Settings(BaseSettings):
    APP_SECRET: str = "secret"
    
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 80
    SERVER_SSL: bool = False

    JIRA_APP_CLIENT_ID: str = None
    JIRA_APP_SECRET: str = None

    TELEGRAM_BOT_TOKEN: str = None
    TELEGRAM_BOT_NAME: str = "JiraNoticeBot"
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: int = 27017
    MONGO_DATABASE: str = "jira_bot_database"
    MONGO_USER: str = None
    MONGO_PASSWORD: str = None

    JIRA_AUTH_SCOPE_LIST: List[str] = [
        "read:jira-user",
        "manage:jira-webhook",
        "read:jira-work",
        "offline_access"
    ]

    class Config:
        env_file = "/Users/kirill/own_projects/jira_notifications_manager/.env"

APP_CONFIG = Settings()
WS_MESSAGE_BUS = AsyncMessageBus()