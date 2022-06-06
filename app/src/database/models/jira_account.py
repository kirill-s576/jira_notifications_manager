from pydantic import BaseModel, Field
from typing import Optional, List
from .general import ObjectIdModelMixin


class JiraToken(BaseModel):
    access_token: str
    refresh_token: str
    scope: str
    expires_in: int
    token_type: str


class AccessibleResource(BaseModel):
    id: str
    name: str
    url: str
    scopes: List[str]
    avatar_url: str = Field(..., alias="avatarUrl")

    class Config:
        allow_population_by_field_name = True


class BaseJiraAccount(BaseModel):
    user_id: str
    resource_id: str
    resource_name: str
    resource_url: Optional[str]
    avatar_url: Optional[str]
    scopes: List[str] = []
    token: Optional[JiraToken]


class JiraAccountRead(BaseJiraAccount, ObjectIdModelMixin):
    ...


class JiraAccountCreate(BaseJiraAccount):
    ...


class JiraAccountUpdate(BaseJiraAccount):
    ...
