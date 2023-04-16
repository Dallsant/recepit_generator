from pydantic import BaseModel

class AuthenticationToken(BaseModel):
    token: str
