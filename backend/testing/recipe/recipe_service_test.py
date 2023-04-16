import pytest as pytest
from config import get_config
from db import db
from testing.test_data import mock_recipe_image, generate_ingredients_list, \
    get_testing_recipe
from recipe.recipe_exceptions import InvalidAmountOfRecipesException, IngredientLimitException, \
    InvalidValidIngredientsException, IngredientIsTooLongException
from recipe.recipe_models import RecipeGenerationParams, Recipe
from recipe.recipe_service import RecipeService
from user.user_repository import get_user_by_email


@pytest.mark.asyncio
async def test_validate_ingredients_integrity():
    # Define valid and invalid ingredient inputs for testing
    valid_ingredients = ["chocolate", "marshmallow"]
    valid_ingredients2 = ["chocolate", "marshmallow", ""]
    invalid_ingredients = ["      ", ""]
    invalid_ingredients2 = ["&^%^%!"]
    sub_ingredients = ["honey, sugar", "caramel"]

    # Create a RecipeService object to test
    recipe_service = RecipeService()

    # Test the method with sub-ingredients and check if the expected number of filtered ingredients is returned
    filtered_ingredients3 = recipe_service.validate_ingredients_integrity(sub_ingredients)
    assert len(filtered_ingredients3) == 3

    # Test the method with valid input ingredients and check if the filtered ingredients match the expected values
    filtered_ingredients = recipe_service.validate_ingredients_integrity(valid_ingredients)
    assert filtered_ingredients == valid_ingredients

    filtered_ingredients2 = recipe_service.validate_ingredients_integrity(valid_ingredients2)
    assert filtered_ingredients2 == valid_ingredients

    # Test the method with invalid ingredients and check that it raises the right exceptions
    with pytest.raises(InvalidValidIngredientsException):
        recipe_service.validate_ingredients_integrity(invalid_ingredients)

    with pytest.raises(InvalidValidIngredientsException):
        recipe_service.validate_ingredients_integrity(invalid_ingredients2)

@pytest.mark.asyncio
async def test_fetch_image_for_recipe(mock_ddg_image_search):
    recipe_service = RecipeService()

    # Get a testing recipe to fetch an image for
    recipe = await get_testing_recipe()

    # Call the fetch_image_for_recipe() method of RecipeService on the recipe
    updated_recipe = await recipe_service.fetch_image_for_recipe(recipe)

    # Check if the recipe's image has been updated to the expected value using an assertion
    assert updated_recipe.image == mock_recipe_image


@pytest.mark.asyncio
async def test_link_images_to_recipes(mock_ddg_image_search):
    recipe_service = RecipeService()
    recipe = await get_testing_recipe()

    updated_recipes = await recipe_service.link_images_to_recipes([recipe, recipe])

    # Verify the image returned is the correct one
    assert updated_recipes[0].image == mock_recipe_image
    assert updated_recipes[1].image == mock_recipe_image


@pytest.mark.asyncio
async def test_save_recipes(mock_ddg_image_search):
    # Create an instance of the RecipeService class
    recipe_service = RecipeService()

    # Get the testing user's email from the configuration
    user = await get_user_by_email(get_config().TESTING_USER_EMAIL)

    # Create two Recipe objects with some sample data
    recipe1 = Recipe(name="name", description="description", ingredients=["ingredient1", "ingredient2"],
                     instructions=["instruction1", "instructions2"])
    recipe2 = Recipe(name="name2", description="description", ingredients=["ingredient1", "ingredient2"],
                     instructions=["instruction1", "instructions2"])

    # Create recipes
    recipes = await recipe_service.save_recipes([recipe1, recipe2], user)

    # Check values are as expected
    assert recipes[0].name == recipe1.name
    assert recipes[0].user_id == user.id

    assert recipes[1].name == recipe2.name
    assert recipes[1].user_id == user.id

    # Delete the two Recipe objects from the database
    await db.delete(recipe1)
    await db.delete(recipe2)
