from pydantic import BaseModel, Field, validator
from bson.objectid import ObjectId
from typing import Union


class ObjectIdModelMixin(BaseModel):
    id: Union[str, ObjectId] = Field(..., alias="_id")

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda x: str(x)
        }

    @validator("id", pre=True)
    def string_to_object_id(cls, val):
        if isinstance(val, ObjectId):
            return val
        else:
            return ObjectId(val)
