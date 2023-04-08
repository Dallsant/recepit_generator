from typing import Optional
from db import db
from user.user_exceptions import UserNotFoundException
from user.user_models import User
from odmantic import query


async def get_user_by_email(email: str, raise_if_not_found: Optional[bool] = True) -> User:
    """
    Get user by Email
    :param email: email
    :param raise_if_not_found: raise exception if not found
    :return: the recipe
    """

    user = await db.find_one(User, query.and_(
        User.email == email,
        query.ne(User.is_deleted, True)
    ))

    if not user and raise_if_not_found:
        raise UserNotFoundException()

    return user
