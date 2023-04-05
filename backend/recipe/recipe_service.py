from typing import List, Any, Dict, Optional, Tuple, Union
import os
import openai
import json
from config import get_config
from recipe.recipe_prompts import recipe_generation_prompt

openai.api_key = get_config().OPENAI_KEY

class RecipeService:
    def __init__(self):
        self.prompt = recipe_generation_prompt.replace("${EXAMPLE_PARAMETERS}",
         str({"strict_mode": True, "output_language": "English", "amount_of_dishes": 1,
          "ingredients":["oreos", "peanuts", "chocolate"], "detailed_directions":False})
          )

    def generate_recipe(self, ingredients:List[str]):

        parameters = {"strict_mode": True, "output_language": "English", "amount_of_dishes": 3,
                           "ingredients":ingredients, "detailed_directions":True}

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.prompt.replace("${PARAMETERS}", str(parameters)),
            temperature=0.7,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        ).get('choices')[0].get('text').replace('\\', '')

        return json.loads(response)

