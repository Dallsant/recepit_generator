from fastapi import APIRouter, Depends, Query
from authentication.authentication_service import AuthenticationService
from user.user_models import RegisterUserParams

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/register")
async def register(params:RegisterUserParams):
    """
    Registers a new user
    """
    auth_service = AuthenticationService()
    return await auth_service.register(params.email, params.password)


@router.post("/login")
async def login(params:RegisterUserParams):
    """
    Authenticates an user
    """
    auth_service = AuthenticationService()
    return await auth_service.login(params.email, params.password)

