from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class User(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    username: str
    password: str
    email: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class UserDBModel(User):
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if self.id:
            data["_id"] = str(data["_id"])
        return data


class LoginPayload(BaseModel):
    username: str
    password: str
