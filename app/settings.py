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


APP_CONFIG = Settings()
WS_MESSAGE_BUS = AsyncMessageBus()

SERVER_HTTP_PROTOCOL = "http" if not APP_CONFIG.SERVER_SSL else "https"


class LogConfig(BaseSettings):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "jira_bot_app"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "jira_bot_app": {"handlers": ["default"], "level": LOG_LEVEL},
    }