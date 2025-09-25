from fastapi import APIRouter, status
from utils.constants import Endpoints, ResponseMessages
from .UserSchemas import UserSchema, UserLoginSchema

UserRouter = APIRouter(prefix="/users", tags=["Users"])

@UserRouter.post(Endpoints.REGISTER)
def create_user(user: UserSchema):
    """
    Endpoint to create a new user.
    """
    print(user)
    # Logic to create a user would go here
    return {"message": ResponseMessages.USER_CREATED, "status": status.HTTP_201_CREATED}

@UserRouter.get(Endpoints.LOGIN)
def login_user(user: UserLoginSchema):
    """
    Endpoint to log in a user.
    """
    return {"message": USER_LOGGED_IN, "status": status.HTTP_200_OK}