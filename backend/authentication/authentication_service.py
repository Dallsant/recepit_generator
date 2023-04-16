from typing import Union
from fastapi import Request

from authentication.authentication_models import AuthenticationToken
from config import get_config
from db import db
from logger import logger
from root_exception import RootException
from user.user_exceptions import UserAlreadyExistsException, InvalidPasswordException
from user.user_models import User, PublicUser
import bcrypt
from user.user_repository import get_user_by_email
import re
from jose import JWTError, jwt


class AuthenticationService:

    def validate_password(self, password) -> bool:
        """
        Validates a password against a regular expression
        :param password: the password to validate
        :return: true if the password is valid, false otherwise
        """

        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        return True if re.match(pattern, password) else False

    def generate_jwt_token(self, user: User) -> AuthenticationToken:
        """
        Generates a JWT token for the given user
        :param user: the user to generate the token for
        :return: the JWT token
        """

        try:
            token = jwt.encode({"email": user.email, "is_admin": user.is_admin},
                               get_config().JWT_TOKEN_KEY,
                               algorithm=get_config  ().JWT_TOKEN_ALGORITHM)
            return AuthenticationToken(token=token)

        except JWTError as e:
            logger.error(f"error while generating jwt token {e.message}")
            raise RootException(f"error during login", 500)

    def get_user_data(self, token: str) -> PublicUser:
        """
        :param token: str
        :return: jwt payload
        """
        return PublicUser(**jwt.decode(token, get_config().JWT_TOKEN_KEY,
                          algorithms=get_config().JWT_TOKEN_ALGORITHM))

    async def get_current_user(self, token: str) -> Union[User, None]:
        """
        :param token: str
        :return: user
        """
        user_data = self.get_user_data(token)
        return await get_user_by_email(user_data.email)

    def hash_password(self, password: str):
        return bcrypt.hashpw(password.encode('utf-8'), get_config().PASSWORD_HASH.encode('utf-8'))

    async def register(self, email: str, password: str) -> PublicUser:
        """
        Registers a new user with the given email and password
        :param email: user email
        :param password: user password
        :return: the registered user
        """

        user = await get_user_by_email(email, raise_if_not_found=False)

        if user:
            raise UserAlreadyExistsException()
        if not self.validate_password(password):
            raise InvalidPasswordException()

        hashed_password = self.hash_password(password)

        new_user = await db.save(User(email=email.lower(), hashed_password=hashed_password))

        return new_user.get_public_user()

    async def login(self, email: str, password: str) -> AuthenticationToken:
        """
        Logs in a user with the given email and password
        :param email: user email
        :param password: user password
        :return: a JWT token
        """

        user = await get_user_by_email(email)

        if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            raise InvalidPasswordException()

        return self.generate_jwt_token(user)


async def authenticate_request(
        request: Request,
) -> Union[None, User]:
    """
    Get current logged-in user from JWT token
    :param request: current request
    :return: User
    """
    token = request.headers.get("Authorization", None).replace("Bearer ", "")
    if not token:
        return

    return await AuthenticationService().get_current_user(token)
