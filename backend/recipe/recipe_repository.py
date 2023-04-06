import asyncio

from db import db
from recipe.recipe_models import Recipe
from odmantic import query, ObjectId


async def get_recipe_by_id(id: str) -> Recipe:
    return await db.find_one(Recipe, query.and_(
        Recipe.id == ObjectId(id),
        query.ne(Recipe.deleted, True)
    ))

async def get_recipes_by_user_id(user_id:str) -> Recipe:
    return await db.find(Recipe, query.and_(
        Recipe.user_id == user_id,
        query.ne(Recipe.deleted, True)
    ))


