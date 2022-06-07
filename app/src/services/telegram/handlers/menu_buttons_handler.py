from src.utils.tg_bot import Dispatcher, types
from settings import APP_CONFIG
from src.services.telegram.bot_service import JiraBotAsyncService


def menu_buttons_handler(dispatcher: Dispatcher, **kwargs) -> Dispatcher:

    bot_service = JiraBotAsyncService(APP_CONFIG.TELEGRAM_BOT_TOKEN)

    @dispatcher.message_handler(lambda message: message.text == "--Info--")
    async def bot_info(message: types.Message):
        """
        This handler will be called if --Info-- menu button pressed.
        """
        await bot_service.send_info_message(message.chat.id)

    @dispatcher.message_handler(lambda message: message.text == "--My accounts--")
    async def my_accounts(message: types.Message):
        """
        This handler will be called if  --My accounts-- menu button pressed.
        """
        await bot_service.send_user_jira_accounts(message.chat.id)

    @dispatcher.message_handler(lambda message: message.text == "--Add account--")
    async def add_account(message: types.Message):
        """
        This handler will be called if  --Add account-- menu button pressed.
        """
        await bot_service.send_message_to_add_jira_account(message.chat.id)

    return dispatcher
