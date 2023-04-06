from db import db
from user.user_models import User
from odmantic import query


async def get_user_by_email(email: str) -> User:
    return await db.find(User, query.and_(
        User.email == email,
        query.ne(User.deleted, True)
    ))