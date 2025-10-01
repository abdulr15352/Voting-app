from fastapi import APIRouter, status, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from utils.constants import Endpoints, ResponseMessages
from utils.security import hash_password, verify_password, create_access_token, decode_access_token
from .UserSchemas import UserSchema, UserLoginSchema, UserRegisterResponseSchema, CandidateSchema, VotingSchema
from db.DbConfig import get_db
from db.DBModels import UserDBModel, CandidateDBModel, VoteDBModel
from sqlalchemy.orm import Session
from sqlalchemy import func


UserRouter = APIRouter(prefix="/users", tags=["Users"])

@UserRouter.post(Endpoints.REGISTER, status_code=status.HTTP_201_CREATED, response_model=UserRegisterResponseSchema)
def create_user(user: UserSchema, db=Depends(get_db)):
    """
    Endpoint to create a new user.
    """
    # validate user 
    existing_user = db.query(UserDBModel).filter(UserDBModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.USER_ALREADY_EXISTS)
    # add user to the database
    hashed_password = hash_password(user.password)
    new_user = UserDBModel(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    db.refresh(new_user)
    return new_user



@UserRouter.get(Endpoints.LOGIN)
def login_user(user: UserLoginSchema, db=Depends(get_db)):
    """
    Endpoint to log in a user.
    """
    # validate user
    existing_user = db.query(UserDBModel).filter(UserDBModel.email == user.email).first()
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
def delete_user(payload = Depends(decode_access_token), db=Depends(get_db)):
    """
    Endpoint to delete a user.
    """
    user_id = payload.get("user_id")
    user = db.query(UserDBModel).filter(UserDBModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.USER_NOT_FOUND)
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"message": ResponseMessages.USER_DELETED, "status": status.HTTP_200_OK}


@UserRouter.post(Endpoints.VOTE, status_code=status.HTTP_201_CREATED)
def vote(candidate: VotingSchema, user = Depends(decode_access_token), db=Depends(get_db)):
    """
    Endpoint to cast a vote for a candidate.
    """
    # Check if candidate exists
    existing_candidate = db.query(CandidateDBModel).filter(CandidateDBModel.id == candidate.candidate_id).first()
    if not existing_candidate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Candidate not found")
    # Check if user has already voted
    user_id = user.get("user_id")
    existing_vote = db.query(VoteDBModel).filter(VoteDBModel.user_id == user_id).first()
    if existing_vote:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already voted")
    # Cast vote
    new_vote = VoteDBModel(user_id=user_id, candidate_id=candidate.candidate_id)
    try:
        db.add(new_vote)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    db.refresh(new_vote)
    return new_vote

AdminRouter = APIRouter(prefix="/admin", tags=["Admin"])

# add candidates to db
@AdminRouter.post(Endpoints.ADD_CANDIDATE, status_code=status.HTTP_201_CREATED)
def add_candidate(new_candidate: CandidateSchema, db=Depends(get_db)):
    candidate = CandidateDBModel(**new_candidate.model_dump())
    try:
        db.add(candidate)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=" The candidate already exists")
    db.refresh(candidate)
    return candidate

@AdminRouter.get("/votes/all-candidates/count")
def get_vote_counts(db=Depends(get_db)):
    # Aggregate votes by candidate_id and candidate name
    results = db.query(CandidateDBModel.name, func.count(VoteDBModel.id).label("vote_count"))\
        .outerjoin(VoteDBModel, CandidateDBModel.id == VoteDBModel.candidate_id)\
        .group_by(CandidateDBModel.id).all()
    print(results)
    return [{"name": name, "vote_count": count} for name, count in results]


# get all candidates
@AdminRouter.get(Endpoints.ADD_CANDIDATE)
def get_candidates(db=Depends(get_db)):
    candidates = db.query(CandidateDBModel).all()
    return candidates