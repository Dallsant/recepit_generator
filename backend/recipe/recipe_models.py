from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from odmantic import EmbeddedModel, Model, Field
from datetime import datetime


class SupportedLanguages(str, Enum):
    spanish = "Spanish"
    english = "English"
    french = "French"
    german = "German"


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
    detailed_instructions: bool = False

    # Amount of dishes to generate
    amount_of_recipes: int = 3


class Recipe(Model):
    # Recipe name
    name: str

    # Linked user to recipe
    user_id: Optional[str] = None

    # Breif deswcription of recipe
    description: Optional[str] = None

    # List of ingredients
    ingredients: List[str] = []

    # instructions to create recipe
    instructions: List[str] = []

    # image irl linked to recipe, currently being generated using duckduckgo_search
    image: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: Optional[bool] = False

    class Config:
        collection = "recipes"
        parse_doc_with_default_factories = True
