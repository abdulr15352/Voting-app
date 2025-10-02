from fastapi import APIRouter, status, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from utils.constants import Endpoints, ResponseMessages
from utils.security import hash_password, verify_password, create_access_token, decode_access_token
from .UserSchemas import UserSchema, UserLoginSchema, UserRegisterResponseSchema, CandidateSchema, VotingSchema
from .UserDBModels import UserDBModel, CandidateDBModel, VoteDBModel, add_user, get_user_by_email, delete_user_by_id, add_candidate as add_candidate_db, get_candidate_by_id, get_all_candidates, add_vote, get_vote_by_user, get_vote_counts


UserRouter = APIRouter(prefix="/users", tags=["Users"])

@UserRouter.post(Endpoints.REGISTER, status_code=status.HTTP_201_CREATED, response_model=UserRegisterResponseSchema)
def create_user(user: UserSchema):
    """
    Endpoint to create a new user.
    """
    # validate user
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.USER_ALREADY_EXISTS)
    # add user to the database
    hashed_password = hash_password(user.password)
    new_user = UserDBModel(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    add_user(new_user)
    return new_user



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




@UserRouter.get(Endpoints.UserInfo)
def get_user_info(payload = Depends(decode_access_token)):
    """
    Endpoint to get user information.
    """
    return payload

@UserRouter.delete(Endpoints.DELETE)
def delete_user(payload = Depends(decode_access_token)):
    """
    Endpoint to delete a user.
    """
    user_id = payload.get("user_id")
    from .UserDBModels import UsersDB
    user = UsersDB.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.USER_NOT_FOUND)
    delete_user_by_id(user_id)
    return {"message": ResponseMessages.USER_DELETED, "status": status.HTTP_200_OK}


@UserRouter.post(Endpoints.VOTE, status_code=status.HTTP_201_CREATED)
def vote(candidate: VotingSchema, user = Depends(decode_access_token)):
    """
    Endpoint to cast a vote for a candidate.
    """
    # Check if candidate exists
    existing_candidate = get_candidate_by_id(candidate.candidate_id)
    if not existing_candidate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Candidate not found")
    # Check if user has already voted
    user_id = user.get("user_id")
    existing_vote = get_vote_by_user(user_id)
    if existing_vote:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already voted")
    # Cast vote
    new_vote = VoteDBModel(user_id=user_id, candidate_id=candidate.candidate_id)
    add_vote(new_vote)
    return new_vote

AdminRouter = APIRouter(prefix="/admin", tags=["Admin"])

# add candidates to db
@AdminRouter.post(Endpoints.ADD_CANDIDATE, status_code=status.HTTP_201_CREATED)
def add_candidate(new_candidate: CandidateSchema):
    candidate = CandidateDBModel(**new_candidate.model_dump())
    add_candidate_db(candidate)
    return candidate

@AdminRouter.get("/votes/all-candidates/count")
def get_vote_counts():
    # Aggregate votes by candidate_id and candidate name
    results = get_vote_counts()
    return results


# get all candidates
@AdminRouter.get(Endpoints.ADD_CANDIDATE)
def get_candidates():
    candidates = get_all_candidates()
    return candidates
