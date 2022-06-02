from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class JiraAccount(BaseModel):
    id: ObjectId
    user_id: str = None
    access_token: str = None
    refresh_token: str = None

    class Config:
        arbitrary_types_allowed = True
