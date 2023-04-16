import pytest
from user.user_models import User


@pytest.fixture
def user():
    return User(
        email="test@example.com",
        picture="http://example.com/pic.jpg",
        is_testing_user=True,
        is_admin=True,
    )

def test_get_public_user(user):
    public_user = user.get_public_user()
    assert public_user.email == "test@example.com"
    assert public_user.picture == "http://example.com/pic.jpg"
    assert public_user.is_admin == True
