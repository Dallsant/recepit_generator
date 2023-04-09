from typing import Union, List

from fastapi import APIRouter, Depends, Query
from authentication.authentication_service import authenticate_request
from recipe.recipe_models import RecipeGenerationParams, Recipe
from recipe.recipe_repository import get_recipe_by_id
from recipe.recipe_service import RecipeService
from user.user_models import User

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)


@router.post("/generate")
async def generate_recipes(params: RecipeGenerationParams) -> List[Recipe]:
    """
    Generates recipes
    """
    recipe_service = RecipeService()
    return await recipe_service.generate_recipes(params)


@router.get("/{recipe_id}")
async def get_recipe(recipe_id: str) -> Recipe:
    """
    Get a recipe by id
    """
    return await get_recipe_by_id(recipe_id)


@router.post("/")
async def save_recipes(recipes: Union[Recipe, List[Recipe]], user: User = Depends(authenticate_request),
                       recipe_service: RecipeService = Depends()) -> List[Recipe]:
    """
    Save a list of recipes and links them to the current yser
    """
    return await recipe_service.save_recipes(recipes, user)
