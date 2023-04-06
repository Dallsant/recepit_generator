from http.client import HTTPException


class RootException(HTTPException):
    def __init__(self, message: str, status_code: int, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

    def __str__(self):
        return self.message or 'An error has occured'