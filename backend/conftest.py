import asyncio
from unittest.mock import patch
import pytest
from starlette.testclient import TestClient
import main
from authentication.authentication_service import AuthenticationService
from db import db
from testing.test_data import mock_openai_recipes_response, mock_recipe_image
from testing.testing_migrations import run_testing_migrations
from user.user_repository import get_user_by_email
import nest_asyncio
from unittest import TestCase, mock


nest_asyncio.apply()

@pytest.fixture()
def test_client():
    yield TestClient(app=main.app)

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def authorized_client(logged_as: str,
                      client: TestClient,
                      event_loop):

    auth_service = AuthenticationService()
    user = event_loop.run_until_complete(get_user_by_email(logged_as))
    token = event_loop.run_until_complete(auth_service.generate_jwt_token(user))
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token.get('token')}",
    }
    yield client

@pytest.fixture
def mock_openai_completion():
    with patch('openai.Completion.create') as mock_create:
        mock_create.return_value = mock_openai_recipes_response
        yield mock_create


@pytest.fixture
def mock_ddg_image_search():
    with patch('duckduckgo_search.ddg_images') as mock_ddg_images:
        mock_ddg_images.return_value = [{"thumbnail": mock_recipe_image}]
        yield mock_ddg_images

def pytest_configure(config):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_testing_migrations())

def pytest_sessionstart(session):
    return

def pytest_sessionfinish(session, exitstatus):
    return

def pytest_unconfigure(config):
    db.client.close()
    return