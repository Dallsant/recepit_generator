from typing import Any, List, Optional
from pydantic import BaseModel
from enum import Enum

class SupportedLanguages(str, Enum)
    spanish = "Spanish"
    english = "English"
    french = "French"

class RecipeGenerationPrompValue(str, Enum):
    example_params = "[[EXAMPLE_PARAMETERS]]"
    params = "[[PARAMETERS]]"

class RecipeGenerationParams(BaseModel):
    # Only use ingredients that appear on the ingredients list
    strict_mode: Optional[bool] = False

    # Language the openai output is going to be written in
    output_language: Optional[str] = SupportedLanguages.english

    # List of ingredients
    ingredients: List[str]

    # Used to tell the model to be more explicit
    detailed_directions: bool = False

    # Amount of dishes to generate
    amount_of_dishes: int = 3



