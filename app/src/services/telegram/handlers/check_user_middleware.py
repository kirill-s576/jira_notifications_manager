from src.utils.tg_bot import Dispatcher, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from src.database.client import with_new_async_mongo_session, MongoSession
from src.database.managers.user import UserAsyncMongoManager
from src.database.models.user import UserCreateModel, TelegramAccount


def check_user_middleware(dispatcher: Dispatcher, **kwargs) -> Dispatcher:
    """
    Adds to message: types.Message object:
     - user_model attribute with actual database user model.
     - user_created attribute, which means:
            True - User has just created.
            False - User has already existed in database.
    """
    class CheckUserMiddleware(BaseMiddleware):

        @staticmethod
        def get_user_model(message: types.Message) -> UserCreateModel:
            return UserCreateModel(
                telegram_account=TelegramAccount(
                    chat_id=message.chat.id,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    username=message.from_user.username,
                    language_code=message.from_user.language_code
                )
            )

        @with_new_async_mongo_session()
        async def on_process_message(
            self,
            message: types.Message,
            data: dict,
            mongo_session: MongoSession
        ):
            user_db_manager = UserAsyncMongoManager(mongo_session)
            user_model = self.get_user_model(message)
            user_model, created = await user_db_manager.get_or_create_user(user_model)
            setattr(message, "user_model", user_model)
            setattr(message, "user_created", created)

    dispatcher.middleware.setup(CheckUserMiddleware())

    return dispatcher
