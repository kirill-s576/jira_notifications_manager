from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional


class JiraAccount(BaseModel):
    id: ObjectId = Field(...)
    user_id: Optional[str]
    access_token: Optional[str]
    refresh_token: Optional[str]

    class Config:
        arbitrary_types_allowed = True
