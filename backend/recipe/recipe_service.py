import asyncio
from typing import List, Union
import openai
import json
from config import get_config
from db import db
from recipe.recipe_models import RecipeGenerationParams, RecipeGenerationPrompValue, Recipe
from recipe.recipe_prompts import recipe_generation_prompt
from user.user_models import User
from duckduckgo_search import ddg_images

openai.api_key = get_config().OPENAI_KEY


class RecipeService:
    def __init__(self):
        self.prompt = recipe_generation_prompt

    def get_example_params(self) -> str:
        """
        Returns an example of a RecipeGenerationParams object as a string
        :return: Recipe params as string
        """

        return str(RecipeGenerationParams(
            strict_mode=True, output_language="English",
            amount_of_dishes=1,
            ingredients=["oreos", "peanuts", "chocolate"],
            detailed_instructions=False
        ).dict())

    async def fetch_image_from_recipe(self, recipe: Recipe) -> Recipe:
        """
        Fetches an image for a given recipe
        :param recipe: recipe
        :return: Recipe with linked image
        """

        image = ddg_images(recipe.name, region='wt-wt', safesearch='Off', size=None,
                           type_image=None, layout=None, license_image=None, max_results=1)[0].get('thumbnail')
        recipe.image = image
        return recipe

    async def link_images_to_recipes(self, recipes: List[Recipe]) -> List[Recipe]:
        """
        Links images to a list of recipes
        :param recipes: recipes
        :return: recipes with linked images
        """

        return await asyncio.gather(*[self.fetch_image_from_recipe(r) for r in recipes])

    async def generate_recipes(self, params: RecipeGenerationParams) -> List[Recipe]:
        """
        :param params: Recipe params
        :return: a list of recipes
        """

        new_prompt = self.prompt.replace(RecipeGenerationPrompValue.params, str(params.dict()))
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=new_prompt,
            temperature=0.7,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        ).get('choices')[0].get('text').replace('\n', '')  # Remove linebreaks as it breaks json formatting

        recipes = [Recipe(**i) for i in json.loads(response).get('recipes')]
        return await self.link_images_to_recipes(recipes)

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
