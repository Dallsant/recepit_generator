from root_exception import RootException


class RecipeCreationException(RootException):
    def __init__(self):
        super().__init__("There's been an error while creating a recipe", 500)


class RecipeNotFoundException(RootException):
    def __init__(self):
        super().__init__("Recipe not found", 404)


class InvalidAmountOfRecipesException(RootException):
    def __init__(self):
        super().__init__("Invalid amount of recipes", 403)


class IngredientLimitException(RootException):
    def __init__(self):
        super().__init__("Maximum limit of ingredients reached", 403)


class InvalidValidIngredientsException(RootException):
    def __init__(self):
        super().__init__("No valid ingredients were given", 400)


class IngredientIsTooLongException(RootException):
    def __init__(self):
        super().__init__("Ingredient name exceeds 30 characters limit", 400)
