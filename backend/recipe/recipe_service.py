import asyncio
from typing import List, Union
import openai
import json
from config import get_config
from db import db
from gpt3 import request_gpt3
from logger import logger
from recipe.recipe_exceptions import InvalidAmountOfRecipesException, IngredientLimitException, \
    InvalidValidIngredientsException, IngredientIsTooLongException, RecipeCreationException
from recipe.recipe_models import RecipeGenerationParams, RecipeGenerationPrompValue, Recipe
from recipe.recipe_prompts import get_recipes_prompt
from user.user_models import User
import duckduckgo_search
import re

openai.api_key = get_config().OPENAI_KEY


class RecipeService:
    def __init__(self):
        self.prompt = get_recipes_prompt()

    async def fetch_image_for_recipe(self, recipe: Recipe) -> Recipe:
        """
        Fetches an image for a given recipe
        :param recipe: recipe
        :return: Recipe with linked image
        """

        image = duckduckgo_search.ddg_images(recipe.name, region='wt-wt', safesearch='Off', size=None,
                                             type_image=None, layout=None, license_image=None, max_results=1)[0].get(
            'thumbnail')
        recipe.image = image
        return recipe

    async def link_images_to_recipes(self, recipes: List[Recipe]) -> List[Recipe]:
        """
        Links images to a list of recipes
        :param recipes: recipes
        :return: recipes with linked images
        """

        return await asyncio.gather(*[self.fetch_image_for_recipe(r) for r in recipes])

    def validate_ingredients_integrity(self, ingredients: Union[str, List[str]]) -> List[str]:
        """
        Validates the ingredients list integrity

        :param ingredients: a list of ingredients
        :return: list of sanitized ingredients

        """
        if isinstance(ingredients, str):
            ingredients = [ingredients]

        sanitized_ingredients = []

        for ingredient in ingredients:
            is_valid_ingredient = ingredient and ingredient.strip() and re.search('[a-zA-Z0-9]{3,}', ingredient)

            if is_valid_ingredient:
                """
                Split the ingredient string by comma and append each sub-ingredient to the list,
                this is to prevent people from adding more than one ingredient on a single string
                """
                sub_ingredients = [sub.strip() for sub in ingredient.split(",")]
                for sub in sub_ingredients:
                    if len(sub) <= 30:
                        sanitized_ingredients.append(sub)
                    else:
                        raise IngredientIsTooLongException()

        if not sanitized_ingredients:
            raise InvalidValidIngredientsException()
        elif len(sanitized_ingredients) > get_config().INGREDIENTS_LIMIT:
            raise IngredientLimitException()

        return sanitized_ingredients

    async def generate_recipes(self, params: RecipeGenerationParams) -> List[Recipe]:
        """
        :param params: Recipe params
        :return: a list of recipes
        """
        # Sanitize the ingredients list
        params.ingredients = self.validate_ingredients_integrity(params.ingredients)

        # Cap recipes amount to reduce costs :)
        invalid_amount_of_recipes = params.amount_of_recipes > get_config().RECIPES_LIMIT or params.amount_of_recipes < 1

        if invalid_amount_of_recipes:
            raise InvalidAmountOfRecipesException()
        if len(params.ingredients) > get_config().INGREDIENTS_LIMIT:
            raise IngredientLimitException()

        prompt = self.prompt.replace(RecipeGenerationPrompValue.params, str(params.dict()))

        try:
            response = request_gpt3(prompt)

            # Remove line-breaks as it breaks json formatting
            formatted_response = response.get('text').replace('\n', '')

            recipes = [Recipe(**i) for i in json.loads(formatted_response).get('recipes')]
            return await self.link_images_to_recipes(recipes)

        except openai.InvalidRequestError as e:
            logger.error(f"Openai request failed {e.error['message']}")
            raise RecipeCreationException()
        except Exception as e:
            logger.error(f"Recipe creation failed {e['message']}")
            raise RecipeCreationException()

    async def save_recipes(self, recipes: Union[Recipe, List[Recipe]], user: User) -> Union[Recipe, List[Recipe]]:
        """
        Saves recipes to the database
        :param recipes: recipes
        :param user: the user to be associated with the recipes
        :return: saved recipes
        """

        if type(recipes) is not list:
            recipes = [recipes]

        updated_recipes = []

        for recipe in recipes:
            recipe.user_id = str(user.id)
            updated_recipes.append(recipe)

        return await db.save_all(updated_recipes)
