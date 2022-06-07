from aiogram import Bot, Dispatcher, types
from typing import Callable


class CustomBot:

    HANDLERS = []

    def __init__(self, token: str):
        self._token = token
        self._dispatcher = None
        self.bot = self._get_bot()
        self.dispatcher = self._get_dispatcher()

    def _get_bot(self):
        bot = Bot(token=self._token)
        Bot.set_current(bot)
        return bot

    def _add_logic_to_dispatcher(self, dp: Dispatcher) -> Dispatcher:
        for handler in self.HANDLERS:
            handler(dp, self)
        return dp

    def _get_dispatcher(self):
        dp = Dispatcher(self.bot)
        Dispatcher.set_current(dp)
        dp = self._add_logic_to_dispatcher(dp)
        return dp

    @staticmethod
    def parse_update_dict(data: dict) -> types.Update:
        return types.Update(**data)

    @classmethod
    def add_handler(cls, handler: Callable[[Dispatcher], Dispatcher]):
        cls.HANDLERS.append(handler)

    async def process_update(self, data: dict):
        update = self.parse_update_dict(data)
        return await self.dispatcher.process_update(update)

