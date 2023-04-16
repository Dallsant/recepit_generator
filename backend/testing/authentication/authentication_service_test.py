import pytest

from authentication.authentication_models import AuthenticationToken
from authentication.authentication_service import AuthenticationService
from config import get_config
from root_exception import RootException
from testing.test_data import get_testing_user
from jose import JWTError, jwt
from unittest.mock import patch
from unittest import TestCase, mock
from db import db
import bcrypt
from user.user_repository import get_user_by_email
from user.user_exceptions import UserAlreadyExistsException, InvalidPasswordException, UserNotFoundException


def test_validate_password():
    auth_service = AuthenticationService()

    # valid password
    assert auth_service.validate_password('Abcdefg1#') == True

    # invalid password - length < 8
    assert auth_service.validate_password('weak1#') == False

    # invalid password - missing uppercase letter
    assert auth_service.validate_password('abcdefg1#') == False

    # invalid password - missing lowercase letter
    assert auth_service.validate_password('ABCDEFG1#') == False

    # invalid password - missing special character
    assert auth_service.validate_password('Abcdefg12') == False

    # invalid password - missing digit
    assert auth_service.validate_password('Abcdefg#') == False

@pytest.mark.asyncio
async def test_generate_jwt_token():
    user = await get_testing_user()

    auth_service = AuthenticationService()

    token = auth_service.generate_jwt_token(user)

    assert isinstance(token, AuthenticationToken)
    assert token.token is not None


@pytest.mark.asyncio
async def test_get_user_data():
    user = await get_testing_user()

    auth_service = AuthenticationService()

    token = auth_service.generate_jwt_token(user)

    user_data = auth_service.get_user_data(token=token.token)

    # Check decoded data is the same as the initial user
    assert user.email == user_data.email


@pytest.mark.asyncio
async def test_get_current_user():

    user = await get_testing_user()

    auth_service = AuthenticationService()

    token = auth_service.generate_jwt_token(user)

    user_data = await auth_service.get_current_user(token=token.token)

    # Check decoded data is the same as the initial user
    assert user.email == user_data.email
    assert user.id == user_data.id

@pytest.mark.asyncio
async def test_register():
    auth_service = AuthenticationService()

    # call the register method with a test email and password
    email = "testing555@example.com"
    password = "MyTestingPassword123aaa!"
    public_user = await auth_service.register(email, password)

    # retrieve the user from the database
    user = await get_user_by_email(email)

    # check that the user was successfully added to the database
    assert user is not None

    # check that the email and hashed_password of the user in the database match the input email and hashed password
    assert user.email == email.lower()
    assert bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))

    # check that the public user returned by the method has the expected email
    assert public_user.email == email

    # check that the public user does not have a hashed_password attribute
    assert not hasattr(public_user, "hashed_password")

    with pytest.raises(UserAlreadyExistsException):
        await auth_service.register(email=email, password=password)

    # delete user
    await db.delete(user)

@pytest.mark.asyncio
async def test_login():
    auth_service = AuthenticationService()
    email = "testing888"
    password = "Testing1221!!"

    user = await auth_service.register(email=email, password=password)

    # Test valid credentials
    jwt_token = await auth_service.login(email=email, password=password)

    # Test a valid jwt is generated
    assert isinstance(jwt_token.token, str)
    assert len(jwt_token.token.split(".")) == 3

    # Test wrong password
    with pytest.raises(InvalidPasswordException):
        await auth_service.login(user.email, "wrong_password")

    # Test wrong email
    with pytest.raises(UserNotFoundException):
        await auth_service.login("wrong_email@example.com", "password123")

    # Delete user
    await db.delete(await get_user_by_email(user.email))