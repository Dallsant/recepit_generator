import pytest

from testing.test_data import get_testing_user
from user.user_exceptions import UserNotFoundException
from user.user_repository import get_user_by_email


@pytest.mark.asyncio
async def test_get_user_by_email():
    # Get testing user
    user = await get_testing_user()

    # Find test user
    found_user = await get_user_by_email(user.email)
    assert found_user.email == user.email

    # Test non existent user
    with pytest.raises(UserNotFoundException):
        await get_user_by_email("userdoesntexist@gmail.com")