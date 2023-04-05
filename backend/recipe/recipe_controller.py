from typing import Optional

from fastapi import APIRouter, Depends, Query

from recipe.recipe_service import RecipeService

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"]
)

@router.get("/")
async def callback():
    recipe_service = RecipeService()

    return recipe_service.generate_recipe(["broccoli", "butter", "cheese"])