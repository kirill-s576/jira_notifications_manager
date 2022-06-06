from src.utils.tg_bot import Dispatcher, types


def template_handler(dispatcher: Dispatcher, **kwargs) -> Dispatcher:

    bot = dispatcher.get_current().bot

    @dispatcher.message_handler()
    async def handle_example(message: types.Message):
        """
        This handler will be called in each case.
        """
        await bot.send_message(message.chat.id, "Example message")

    return dispatcher
