from typing import Optional, List, Union
from db import db
from recipe.recipe_exceptions import RecipeNotFoundException
from recipe.recipe_models import Recipe
from odmantic import query, ObjectId


async def get_recipe_by_id(recipe_id: Union[str, ObjectId], raise_if_not_found: Optional[bool] = True) -> Recipe:
    """
    Get a recipe by Id
    :param recipe_id: recipe Id
    :param raise_if_not_found: raise exception if not found
    :return: recipe
    """

    recipe = await db.find_one(Recipe, query.and_(
        Recipe.id == ObjectId(recipe_id),
        query.ne(Recipe.is_deleted, True)
    ))

    if not recipe and raise_if_not_found:
        raise RecipeNotFoundException()

    return recipe


async def get_recipes_by_user_id(user_id: Union[str, ObjectId]) -> List[Recipe]:
    """
    Get recipes by Id
    :param user_id: user Id
    :return: list of recipes
    """

    recipes = await db.find(Recipe, query.and_(
        Recipe.user_id == ObjectId(user_id),
        query.ne(Recipe.is_deleted, True)
    ))

    return recipes or []
