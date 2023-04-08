from typing import Optional
from odmantic import EmbeddedModel, Model, Field
from pydantic import BaseModel
from datetime import datetime


class PublicUser(BaseModel):
    # User email
    email: str

    # User picture url
    picture: Optional[str] = None

    # Check if the user is an admin
    is_admin: Optional[bool] = False

    is_deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(Model):
    # User email
    email: str

    # User picture url
    picture: Optional[str] = None

    # Check if it's a testing account
    is_testing_user: Optional[bool] = False

    # Check if the user is an admin
    is_admin: Optional[bool] = False

    # Hashed password
    hashed_password: Optional[str] = None

    # Filter-out fields that should not be public
    def get_public_user(self):
        return PublicUser(**dict(self))

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = False

    class Config:
        collection = "users"
        parse_doc_with_default_factories = True



class RegisterUserParams(BaseModel):
    # User email
    email: str

    # User password
    password: str
