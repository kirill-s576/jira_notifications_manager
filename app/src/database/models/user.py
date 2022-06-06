from pydantic import BaseModel
from enum import Enum
from typing import Optional
from .general import ObjectIdModelMixin


class UserRoles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class TelegramAccount(BaseModel):
    chat_id: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]


class UserBaseModel(BaseModel):
    role: UserRoles = UserRoles.USER
    telegram_account: Optional[TelegramAccount]


class UserCreateModel(UserBaseModel):
    ...


class UserReadModel(UserBaseModel, ObjectIdModelMixin):
    ...
