from logger import logger
from testing.testing_migrations import create_testing_user


async def run_initial_migrations():
    logger.info("Generating initial migrations")
    await create_testing_user(email="edallsant@gmail.com", password="123456", is_admin=True)
