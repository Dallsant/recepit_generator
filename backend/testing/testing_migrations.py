from typing import Optional
from authentication.authentication_service import AuthenticationService
from config import get_config
from db import db
from logger import logger
from recipe.recipe_models import Recipe
from user.user_models import User
from user.user_repository import get_user_by_email
from odmantic import query, ObjectId


async def create_testing_user(email: str, password: str, is_admin: Optional[bool] = False):
    auth_service = AuthenticationService()
    user = await get_user_by_email(email, raise_if_not_found=False)

    if not user:
        user = await db.save(User(email=email, is_admin=is_admin, hashed_password=auth_service.hash_password(password)))
        logger.info(f"Testing user {user.email} created")

    return user


async def create_testing_recipe():
    recipe = db.find_one(Recipe, Recipe.name == ObjectId(get_config().TESTING_RECIPE_NAME))

    if not recipe:
        recipe = await db.save(Recipe(name=get_config().TESTING_RECIPE_NAME, description="Recipe description",
                                      ingredients=["chocolate", "cream"],
                                      instructions=["Put chocolate and cream in a bowl", "Mix together",
                                                    "Serve in a cup"]))
        logger.info(f"Testing recipe Generated")

    return recipe


async def run_testing_migrations():
    await create_testing_user("testing@testing.com", password="123456", is_admin=False)
    await create_testing_recipe()
