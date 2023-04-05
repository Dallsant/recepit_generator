import openai
import json
from config import get_config
from recipe.recipe_models import RecipeGenerationParams, RecipeGenerationPrompValue
from recipe.recipe_prompts import recipe_generation_prompt

openai.api_key = get_config().OPENAI_KEY


class RecipeService:
    def __init__(self):
        self.prompt = recipe_generation_prompt

    def get_example_params(self):
        return str(RecipeGenerationParams(
            strict_mode=True, output_language="English",
            amount_of_dishes=1,
            ingredients=["oreos", "peanuts", "chocolate"],
            detailed_directions=False
        ).dict())

    def generate_recipe(self, params: RecipeGenerationParams):
        print(params)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.prompt.replace(RecipeGenerationPrompValue.params, str(params.dict())),
            temperature=0.7,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        ).get('choices')[0].get('text').replace('\\', '')
        print(response)
        return json.loads(response)
