from typing import Optional
from authentication.authentication_service import AuthenticationService
from config import get_config
from db import db
from logger import logger
from recipe.recipe_models import Recipe
from user.user_models import User
from user.user_repository import get_user_by_email

async def create_testing_user(email: str, password: str, is_admin: Optional[bool] = False):
    auth_service = AuthenticationService()
    user = await get_user_by_email(email, raise_if_not_found=False)

    if not user:
        user = await db.save(User(email=email, is_admin=is_admin, hashed_password=auth_service.hash_password(password)))
        logger.info(f"Testing user {user.email} created")

    return user


async def create_testing_recipe():
    recipe = await db.find_one(Recipe, Recipe.name == get_config().TESTING_RECIPE_NAME)
    user = await get_user_by_email(get_config().TESTING_USER_EMAIL)

    if not recipe:
        recipe = await db.save(Recipe(name=get_config().TESTING_RECIPE_NAME, description="Recipe description",
                                      ingredients=["chocolate", "cream"],
                                      instructions=["Put chocolate and cream in a bowl", "Mix together",
                                                    "Serve in a cup"], user_id=str(user.id)))
        logger.info(f"Testing recipe Generated")
    return recipe

async def run_testing_migrations():
    await create_testing_user(get_config().TESTING_USER_EMAIL, password="123456", is_admin=False)
    await create_testing_recipe()
