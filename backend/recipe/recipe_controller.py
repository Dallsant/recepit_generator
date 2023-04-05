from fastapi import APIRouter, Depends, Query
from recipe.recipe_models import RecipeGenerationParams
from recipe.recipe_service import RecipeService

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"]
)

@router.post("/")
async def create_recipe(params: RecipeGenerationParams):
    recipe_service = RecipeService()
    return recipe_service.generate_recipe(params)
