from src.utils.tg_bot import CustomBot
from settings import APP_CONFIG
from src.services.telegram.handlers import (
    commands_handler,
    check_user_middleware,
    menu_buttons_handler
)
from src.exceptions.telegram import TokenDoesNotAvailableException


class JiraBotAsyncService(CustomBot):

    HANDLERS = [
        check_user_middleware,
        commands_handler,
        menu_buttons_handler
    ]

    def __init__(self, token: str):
        if token != APP_CONFIG.TELEGRAM_BOT_TOKEN:
            raise TokenDoesNotAvailableException(
                "Token does not supported by the application."
            )
        super().__init__(token)
