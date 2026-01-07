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


class LoginPayload(BaseModel):
    username: str
    password: str
