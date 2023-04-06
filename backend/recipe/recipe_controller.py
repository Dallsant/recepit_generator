from fastapi import APIRouter, Depends, Query
from recipe.recipe_models import RecipeGenerationParams
from recipe.recipe_repository import get_recipe_by_id
from recipe.recipe_service import RecipeService

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"]
)

@router.post("/")
async def create_recipe(params: RecipeGenerationParams):
    recipe_service = RecipeService()
    return recipe_service.generate_recipe(params)


@router.get("/")
async def get_recipe():
    return await get_recipe_by_id("642dfc62445f892a26b27bdd")


