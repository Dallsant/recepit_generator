import pytest
from db import db
from recipe.recipe_exceptions import RecipeNotFoundException
from recipe.recipe_models import Recipe
from recipe.recipe_repository import get_recipe_by_id, get_recipes_by_user_id
from testing.test_data import get_testing_recipe, get_testing_user


@pytest.mark.asyncio
async def test_get_recipe_by_id():
    # Get a testing recipe
    testing_recipe = await get_testing_recipe()

    # Check that the recipe was found
    recipe = await get_recipe_by_id(testing_recipe.id)
    assert testing_recipe.id == recipe.id

    # Create a new recipe and save it to the database
    new_recipe = Recipe(name="test")

    # Save the new recipe to the database
    await db.save(new_recipe)

    # Check that the new recipe was successfully saved to the database
    assert await get_recipe_by_id(new_recipe.id)

    # Delete the new recipe from the database
    await db.delete(new_recipe)

    # Check that the recipe was successfully deleted and raises an exception when not found
    with pytest.raises(RecipeNotFoundException):
        await get_recipe_by_id(new_recipe.id)


@pytest.mark.asyncio
async def test_get_recipe_by_user_id():
    # Get a testing recipe
    testing_recipe = await get_testing_recipe()

    # Get a testing user
    user = await get_testing_user()

    # Create a new recipe and associate it with the testing user
    new_recipe = Recipe(name="test", user_id=user.id)

    # Save the new recipe to the database
    await db.save(new_recipe)

    # Get all recipes associated with the testing user
    recipes = await get_recipes_by_user_id(user.id)

    # Check that the testing recipe and the new recipe are in the list of recipes associated with the user
    assert str(testing_recipe.id) in [str(recipe.id) for recipe in recipes]
    assert str(new_recipe.id) in [str(recipe.id) for recipe in recipes]

    # Check that the correct number of recipes associated with the user are returned
    assert len(recipes) == 2

    # Delete the new recipe from the database
    await db.delete(new_recipe)

    # Check that the correct number of recipes associated with the user are returned after the deletion
    recipes2 = await get_recipes_by_user_id(user.id)
    assert len(recipes2) == 1
