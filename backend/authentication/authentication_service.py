from config import get_config
from db import db
from user.user_exceptions import UserAlreadyExistsException, InvalidPasswordException
from user.user_models import User
import bcrypt
from user.user_repository import get_user_by_email
import re


class AuthenticationService:

    def _validate_password(self, password):
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        return re.match(pattern, password)

    async def register(self, email: str, password: str):
        user = await get_user_by_email(email)
        if user:
            raise UserAlreadyExistsException()
        if not self._validate_password(password):
            raise InvalidPasswordException()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), get_config().PASSWORD_HASH.encode('utf-8'))

        new_user = await db.save(User(email=email.lower(), hashed_password=hashed_password))

        return new_user.get_public_user()

    async def login(self, email: str, password: str):
        user = await get_user_by_email(email)
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            print('Password Matched!')
        else:
            print('Incorrect Password')

    #     return user
