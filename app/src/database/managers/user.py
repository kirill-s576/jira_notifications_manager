from .base import BaseAsyncMongoManager
from ..models.user import UserCreateModel, UserReadModel


class UserAsyncMongoManager(BaseAsyncMongoManager):

    async def create_user(self, user: UserCreateModel):
        pass

    async def get_user(self) -> UserReadModel:
        pass

