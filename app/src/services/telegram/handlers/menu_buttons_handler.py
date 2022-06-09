from src.utils.tg_bot import Dispatcher, types


def menu_buttons_handler(dispatcher: Dispatcher, bot_service, **kwargs) -> Dispatcher:

    @dispatcher.message_handler(lambda message: message.text == "--Info--")
    async def bot_info(message: types.Message):
        """
        This handler will be called if --Info-- menu button pressed.
        """
        await bot_service.send_info_message(message.chat.id)

    @dispatcher.message_handler(lambda message: message.text == "--Add account--")
    async def add_account(message: types.Message):
        """
        This handler will be called if  --Add account-- menu button pressed.
        """
        await bot_service.send_message_to_add_jira_account(message.chat.id)

    return dispatcher
