from src.utils.tg_bot import Dispatcher, types
from settings import APP_CONFIG
from src.services.telegram.bot_service import JiraBotAsyncService


def commands_handler(dispatcher: Dispatcher, **kwargs) -> Dispatcher:
    """
    Handler handles service commands "/..."
    """
    bot_service = JiraBotAsyncService(APP_CONFIG.TELEGRAM_BOT_TOKEN)

    @dispatcher.message_handler(commands=['start'])
    async def on_start(message: types.Message):
        """
        This handler will be called when user sends `/start`
        - Return welcome message.
        - Show menu.
        - If user have accounts - Show WebApp to manage settings.
        """
        await bot_service.send_welcome_message_with_regular_menu(message.chat.id)

    @dispatcher.message_handler(commands=['help'])
    async def on_help(message: types.Message):
        """
        This handler will be called when user sends `/help`
        - Return information about the service.
        """
        await bot_service.send_help_message(message.chat.id)

    return dispatcher


