from root_exception import RootException


class RecipeCreationException(RootException):
    def __init__(self):
        super().__init__("There's been an error while creating a recipe", 500)


class RecipeNotFoundException(RootException):
    def __init__(self):
        super().__init__("Recipe not found", 404)

