from recipe.recipe_models import Recipe
from pydantic import ValidationError
import pytest

@pytest.fixture
def ingredients():
    return ["bananas", "chocolate", "strawberry", "caramel"]

@pytest.fixture
def instructions():
    return ["instruction1", "instruction2", "instruction3", "instruction4", "instruction5"]

@pytest.fixture
def recipe_dict(ingredients, instructions):
    return {
        "name": "Test recipe",
        "description": "This is a test description",
        "ingredients": ingredients,
        "instructions": instructions,
        "image": "https://www.budgetbytes.com/wp-content/uploads/2022/06/No-Churn-Strawberry-Ice-Cream-V2-768x1024.jpg",
    }

def test_recipe_model(recipe_dict, ingredients, instructions):
    # Test valid input
    recipe = Recipe(**recipe_dict)

    assert recipe.name == "Test recipe"
    assert recipe.ingredients == ingredients
    assert recipe.instructions == instructions
    assert recipe.description == "This is a test description"

    # Test invalid input
    with pytest.raises(ValidationError):
        recipe.name = None

    # Validate that an invalid image gets removed
    recipe.image = "testing"
    assert recipe.image is None