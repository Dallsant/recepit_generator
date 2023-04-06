from typing import Optional
from odmantic import EmbeddedModel, Model, Field
from pydantic import BaseModel
from datetime import datetime


class PublicUser(BaseModel):
    email: str
    picture: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted: bool = False
    is_admin: Optional[bool] = False

class User(Model):
    email: str
    picture: Optional[str] = None
    is_testing_user: Optional[bool] = False
    is_admin: Optional[bool] = False
    hashed_password: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted: bool = False

    def get_public_user(self):
        return PublicUser(**dict(self))

    class Config:
        collection = "users"
        parse_doc_with_default_factories = True



class RegisterUserParams(BaseModel):
    email: str
    password: str
