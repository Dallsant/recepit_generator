import asyncio

import pytest
from starlette.testclient import TestClient

import main
from db import db


@pytest.fixture()
def test_client():
    yield TestClient(app=main.app)

async def clear_all_db_collections():
    testing_db = db().get_client()
    collections = await testing_db.list_collection_names()
    for collection in collections:
        logger.debug(f"Dropping collection '{collection}'")
        await testing_db[collection].drop()
    await database.setup()

def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """



    loop = asyncio.get_event_loop()
    loop.run_until_complete(clear_all_db_collections())
    loop.run_until_complete(testing_migrations())

def pytest_sessionstart(session):
    return

def pytest_unconfigure(config):
    db.close()
    return