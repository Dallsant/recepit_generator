from typing import Optional
from odmantic import EmbeddedModel, Model, Field


class User(Model):
    email: str
    picture: Optional[str] = None
    is_test_user: Optional[bool] = False
    deleted: Optional[bool] = False
    is_admin: Optional[bool] = False

    class Config:
        collection = "users"
        parse_doc_with_default_factories = True