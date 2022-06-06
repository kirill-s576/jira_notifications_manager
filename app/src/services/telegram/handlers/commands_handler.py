from src.utils.tg_bot import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def commands_handler(dispatcher: Dispatcher, **kwargs) -> Dispatcher:
    """
    Handler handles service commands "/..."
    """
    bot = dispatcher.get_current().bot

    def get_menu_keyboard_markup():
        keyboard_markup = ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton("--Info--"),
                    KeyboardButton("--Add account--")
                ],
                [
                    KeyboardButton("--My accounts--"),
                ]
            ],
            row_width=3,
            resize_keyboard=True
        )
        return keyboard_markup

    @dispatcher.message_handler(commands=['start'])
    async def on_start(
            message: types.Message
    ):
        """
        This handler will be called when user sends `/start`
        - Return welcome message.
        - Show menu.
        -
        """
        print("ON_START")
        await bot.send_message(
            message.chat.id,
            "Welcome to Jira Notifications Bot",
            reply_markup=get_menu_keyboard_markup()
        )

    @dispatcher.message_handler(commands=['help'])
    async def on_help(message: types.Message):
        """
        This handler will be called when user sends `/help`
        - Return information about the service.
        """
        await bot.send_message(message.chat.id, "Coming soon...")

    return dispatcher


