from src.utils.tg_bot import CustomBot
from src.services.telegram.handlers import (
    commands_handler
)


class JiraBot(CustomBot):

    HANDLERS = [
        commands_handler
    ]


