from pydantic import BaseModel
from enum import Enum


class UserRoles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class TelegramAccount(BaseModel):
    client_id: str
    username: str


class User(BaseModel):
    role: UserRoles = UserRoles.USER
    telegram_account: TelegramAccount

    class Config:
        use_enum_values = True
