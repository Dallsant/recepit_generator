from fastapi import APIRouter, Depends, Query

from authentication.authentication_service import AuthenticationService
from recipe.recipe_models import RecipeGenerationParams
from recipe.recipe_repository import get_recipe_by_id
from recipe.recipe_service import RecipeService
from user.user_models import RegisterUserParams

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register")
async def register(params:RegisterUserParams):
    auth_service = AuthenticationService()
    return await auth_service.register(params.email, params.password)


@router.post("/login")
async def register(params:RegisterUserParams):
    auth_service = AuthenticationService()
    return await auth_service.login(params.email, params.password)

@router.get("/")
async def get_recipe():
    return await get_recipe_by_id("642dfc62445f892a26b27bdd")
