from src.utils.tg_bot import Dispatcher, types
from src.database.client import with_new_async_mongo_session, MongoSession
from src.database.managers.jira_account import JiraAccountAsyncMongoManager


def menu_buttons_handler(dispatcher: Dispatcher, **kwargs) -> Dispatcher:

    bot = dispatcher.get_current().bot

    def get_auth_button_keyboard_markup(user_state: str):
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                "Login",
                url=f"https://k.dserdiuk.com/jira_auth/login?user_state={user_state}"
            )
        )
        return keyboard

    @dispatcher.message_handler(lambda message: message.text == "--Info--")
    async def add_account(message: types.Message):
        """
        This handler will be called in each case.
        """
        await bot.send_message(message.chat.id, "Example message")

    @dispatcher.message_handler(lambda message: message.text == "--My accounts--")
    @with_new_async_mongo_session()
    async def my_accounts(message: types.Message, mongo_session: MongoSession):
        """
        This handler will be called in each case.
        """
        db_manager = JiraAccountAsyncMongoManager(mongo_session)
        user_id = getattr(message, "user_model").telegram_account.chat_id
        accounts = await db_manager.get_user_accounts(user_id=user_id)
        await bot.send_message(message.chat.id, "There are your accounts: ")
        for account in accounts:
            await bot.send_message(
                message.chat.id,
                f"Id: {str(account.id)} \nRes.Name: {account.resource_name} \nRes. Id: {account.resource_id}"
            )

    @dispatcher.message_handler(lambda message: message.text == "--Add account--")
    async def add_account(message: types.Message):
        """
        This handler will be called in each case.
        """
        keyboard = get_auth_button_keyboard_markup(user_state=message.chat.id)
        await bot.send_message(
            message.chat.id, "Login with Jira", reply_markup=keyboard
        )

    return dispatcher
