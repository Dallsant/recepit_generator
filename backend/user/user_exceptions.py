from root_exception import RootException


class UserAlreadyExistsException(RootException):
    def __init__(self):
        super().__init__("User already exists", 409)

class InvalidPasswordException(RootException):
    def __init__(self):
        super().__init__("Invalid password", 401)

class UserNotFoundException(RootException):
    def __init__(self):
        super().__init__("User not found", 401)