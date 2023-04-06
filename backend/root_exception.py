from fastapi import HTTPException


class RootException(HTTPException):
    def __init__(self, message: str, status_code: int, error_code: str = None):
        self.detail = message
        self.status_code = status_code
        self.error_code = error_code

    def __str__(self):
        return self.detail or 'An unexpected error has occured'