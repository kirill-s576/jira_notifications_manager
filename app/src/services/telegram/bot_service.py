from aiogram import types
from settings import APP_CONFIG, SERVER_HTTP_PROTOCOL
from src.utils.tg_bot import CustomBot
from src.services.telegram.handlers import (
    commands_handler,
    check_user_middleware,
    menu_buttons_handler
)
from src.database.client import with_new_async_mongo_session, MongoSession
from src.database.managers.jira_account import JiraAccountAsyncMongoManager
from src.exceptions.telegram import TokenDoesNotAvailableException


class JiraBotAsyncService(CustomBot):

    HANDLERS = [
        check_user_middleware,
        commands_handler,
        menu_buttons_handler
    ]

    def __init__(self, token: str):
        if token != APP_CONFIG.TELEGRAM_BOT_TOKEN:
            raise TokenDoesNotAvailableException(
                "Token does not supported by the application."
            )
        super().__init__(token)

    async def send_welcome_message_with_regular_menu(self, chat_id: str):
        await self.bot.set_accounts_settings_web_app()
        await self.bot.send_message(
            chat_id=chat_id,
            text="Welcome to Jira Notifications Bot",
            reply_markup=self._get_regular_menu_markup()
        )

    async def send_help_message(self, chat_id: str):
        await self.bot.send_message(
            chat_id=chat_id,
            text="Coming soon..."
        )

    async def send_message_to_add_jira_account(self, chat_id: str):
        keyboard = self._get_auth_button_keyboard_markup(user_state=chat_id)
        await self.bot.send_message(
            chat_id=chat_id,
            text="Login with Jira",
            reply_markup=keyboard
        )

    async def send_info_message(self, chat_id: str):
        await self.bot.send_message(
            chat_id=chat_id,
            text="Info coming soon..."
        )

    async def send_user_jira_accounts(self, chat_id: str):
        accounts = await self._get_user_jira_accounts(chat_id=chat_id)
        await self.bot.send_message(chat_id, "There are your accounts: ")
        for account in accounts:
            text = f"Id: {str(account.id)} \n" \
                   f"Res.Name: {account.resource_name} \n" \
                   f"Res. Id: {account.resource_id}"
            await self.bot.send_message(
                chat_id=chat_id,
                text=text
            )

    async def set_accounts_settings_web_app(self, chat_id: str):
        menu_button = self._get_settings_web_app_menu_button()
        await self.bot.set_chat_menu_button(
            chat_id,
            menu_button
        )

    async def remove_web_app(self, chat_id: str):
        await self.bot.set_chat_menu_button(chat_id, None)

    @staticmethod
    def _get_settings_web_app_menu_button() -> types.MenuButtonWebApp:
        web_app = types.WebAppInfo(
            url="https://k.dserdiuk.com/web_app/jira_accounts"
        )
        menu_button = types.MenuButtonWebApp(
            text="App",
            web_app=web_app
        )
        return menu_button

    @with_new_async_mongo_session()
    async def _get_user_jira_accounts(self, chat_id: str, mongo_session: MongoSession):
        db_manager = JiraAccountAsyncMongoManager(mongo_session)
        accounts = await db_manager.get_user_accounts(user_id=str(chat_id))
        return accounts

    @staticmethod
    def _get_auth_button_keyboard_markup(user_state: str) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                "Login",
                url=f"{SERVER_HTTP_PROTOCOL}://{APP_CONFIG.SERVER_HOST}/jira_auth/login?user_state={user_state}"
            )
        )
        return keyboard

    @staticmethod
    def _get_regular_menu_markup() -> types.ReplyKeyboardMarkup:
        keyboard_markup = types.ReplyKeyboardMarkup(
            [
                [
                    types.KeyboardButton("--Info--"),
                    types.KeyboardButton("--Add account--")
                ],
                [
                    types.KeyboardButton("--My accounts--"),
                ]
            ],
            row_width=3,
            resize_keyboard=True
        )
        return keyboard_markup
