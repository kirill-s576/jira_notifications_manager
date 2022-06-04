from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional


class JiraToken(BaseModel):
    access_token: str
    refresh_token: str
    scope: str
    expires_in: int
    token_type: str


class BaseJiraAccount(BaseModel):
    user_id: Optional[str]
    token: Optional[JiraToken]

    class Config:
        arbitrary_types_allowed = True


class JiraAccountRead(BaseJiraAccount):
    id: ObjectId = Field(...)


class JiraAccountCreate(BaseJiraAccount):
    ...
