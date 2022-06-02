
from aiogram import Bot, Dispatcher, executor, types
import asyncio


class TelegramBotAsyncApi:

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.bot_object = Bot(token=bot_token)

    async def webhook_status(self):
        r = await self.bot_object.get_webhook_info()
        return r

    async def set_webhook(self, webhook_uri: str):
        pass

    async def remove_webhook(self):
        pass
