from fastapi import APIRouter, status, HTTPException
from utils.constants import Endpoints, ResponseMessages
from utils.security import hash_password, verify_password, create_access_token, decode_access_token
from .UserSchemas import UserSchema, UserLoginSchema
from v1.users.UserDBModels import UserDBModel, get_user_by_email, add_user

UserRouter = APIRouter(prefix="/users", tags=["Users"])

@UserRouter.post(Endpoints.REGISTER, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    """
    Endpoint to create a new user.
    """
    # validate user 
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.USER_ALREADY_EXISTS)
    # add user to the database
    new_user = add_user(UserDBModel(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),  # Hash the password before storing
        is_active=user.is_active
    ))
    return {"message": ResponseMessages.USER_CREATED, "status": status.HTTP_201_CREATED}



@UserRouter.get(Endpoints.LOGIN)
def login_user(user: UserLoginSchema):
    """
    Endpoint to log in a user.
    """
    # validate user
    existing_user = get_user_by_email(user.email)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.USER_NOT_FOUND)
    
    # verify password
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessages.INVALID_CREDENTIALS)
    # Generate JWT token
    payload = {
        "user_id": existing_user.id,
        "email": existing_user.email}
    token = create_access_token(data=payload)
    return {"message": ResponseMessages.USER_LOGGED_IN, "token": token, "authentication_type" :"Bearer"}