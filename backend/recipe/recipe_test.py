import pytest as pytest
from unittest.mock import patch

from config import get_config
from testing.test_data import mock_openai_recipes_response, mock_recipe_image, generate_ingredients_list
from recipe.recipe_exceptions import InvalidAmountOfRecipesException, IngredientLimitException, \
    InvalidValidIngredientsException, IngredientIsTooLongException
from recipe.recipe_models import RecipeGenerationParams
from recipe.recipe_service import RecipeService
from faker import Faker

fake = Faker()

@pytest.fixture
def mock_openai_completion():
    with patch('openai.Completion.create') as mock_create:
        mock_create.return_value = mock_openai_recipes_response
        yield mock_create


@pytest.fixture
def mock_ddg_image_search():
    with patch('duckduckgo_search.ddg_images') as mock_ddg_images:
        mock_ddg_images.return_value = [{"thumbnail": mock_recipe_image}]
        yield mock_ddg_images


@pytest.mark.asyncio
async def test_generate_recipes(mock_openai_completion, mock_ddg_image_search):
    recipe_service = RecipeService()

    recipes = await recipe_service.generate_recipes(
        RecipeGenerationParams(amount_of_recipes=4, ingredients=["onions", "oyster sauce", "ginger"]))

    assert recipes[0].image == mock_recipe_image
    assert recipes[0].user_id is None
    assert len(recipes) == 4
    assert recipes[1].name =="Ginger Onion Salad"

    valid_ingredients = ["chocolate", "marshmallow"]
    invalid_ingredients = ["      ", ""]
    invalid_ingredients2 = ["&^%^%!"]

    with pytest.raises(InvalidAmountOfRecipesException):
        await recipe_service.generate_recipes(
            RecipeGenerationParams(amount_of_recipes=0, ingredients=valid_ingredients))

    with pytest.raises(InvalidAmountOfRecipesException):
        await recipe_service.generate_recipes(
            RecipeGenerationParams(amount_of_recipes=get_config().RECIPES_LIMIT + 1, ingredients=valid_ingredients))

    with pytest.raises(IngredientLimitException):
        await recipe_service.generate_recipes(
            RecipeGenerationParams(amount_of_recipes=2, ingredients=generate_ingredients_list(50)))

    with pytest.raises(InvalidValidIngredientsException):
        await recipe_service.generate_recipes(
            RecipeGenerationParams(amount_of_recipes=2, ingredients=invalid_ingredients))

    with pytest.raises(InvalidValidIngredientsException):
        await recipe_service.generate_recipes(
            RecipeGenerationParams(amount_of_recipes=2, ingredients=invalid_ingredients2))

    with pytest.raises(IngredientIsTooLongException):
        await recipe_service.generate_recipes(RecipeGenerationParams(amount_of_recipes=2, ingredients=["Hey, this is "
                                                                                                       "an invalid "
                                                                                                       "ingredients "
                                                                                                       "because it's "
                                                                                                       "too long"]))
