from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from bson import ObjectId


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

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


class UserCreateModel(UserBaseModel):
    ...


class UserReadModel(UserBaseModel):
    id: ObjectId = Field(...)

