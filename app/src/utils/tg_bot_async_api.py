

class TelegramBotAsyncApi:

    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    async def set_webhook(self, webhook_uri: str):
        pass

    async def remove_webhook(self):
        pass
