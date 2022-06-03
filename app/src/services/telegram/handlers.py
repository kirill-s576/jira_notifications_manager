from src.utils.tg_bot import Dispatcher, types


def commands_handler(dispatcher: Dispatcher) -> Dispatcher:

    bot = dispatcher.get_current().bot

    @dispatcher.message_handler(commands=['start'])
    async def handle_start(message: types.Message):
        """
        This handler will be called when user sends `/start`
        """
        await bot.send_message(message.chat.id, "Welcome to Jira Notifications Bot")

    @dispatcher.message_handler(commands=['help'])
    async def handle_start(message: types.Message):
        """
        This handler will be called when user sends `/help`
        """
        await bot.send_message(message.chat.id, "Coming soon...")

    return dispatcher