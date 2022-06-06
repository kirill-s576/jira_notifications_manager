from bson import ObjectId
from typing import Optional, Tuple

from .base import BaseAsyncMongoManager
from ..models.user import UserCreateModel, UserReadModel


class UserAsyncMongoManager(BaseAsyncMongoManager):

    COLLECTION_NAME = "users"

    async def get_or_create_user(self, user: UserCreateModel) -> Tuple[UserReadModel, bool]:
        """
        Telegram account required.
        Method checks telegram chat_id to avoid of user duplication.
        Returns Tuple: (user_model, created or not)
        """
        chat_id = user.telegram_account.chat_id
        exist_user = await self.get_user_by_telegram_chat_id(chat_id=chat_id)
        user_data = user.dict(by_alias=True)
        if not exist_user:
            object_id = await self.create_object(user_data)
            response = UserReadModel(id=object_id, **user_data)
            return response, True
        return exist_user, False

    async def get_user_by_telegram_chat_id(self, chat_id: str) -> Optional[UserReadModel]:
        filter_query = {
            "telegram_account.chat_id": chat_id
        }
        data = await self.collection.find_one(filter_query, session=self.session)
        if not data:
            return None
        response = UserReadModel(**data)
        return response

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[UserReadModel]:
        validated_id = self.validate_id(user_id)
        dict_data = await self.get_object_by_id(object_id=validated_id)
        if not dict_data:
            return None
        return UserReadModel(**dict_data)


