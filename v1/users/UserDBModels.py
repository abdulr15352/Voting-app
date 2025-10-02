from pydantic import BaseModel, EmailStr
from typing import Optional

class UserDBModel(BaseModel):
    id: int = 0
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True

class CandidateDBModel(BaseModel):
    id: int = 0
    name: str
    party: Optional[str] = "Independent"

class VoteDBModel(BaseModel):
    id: int = 0
    user_id: int
    candidate_id: int

# Key: uid, value: UserDBModel, create empty dictionary to simulate a database
UsersDB = {}
CandidatesDB = {}
VotesDB = {}

def get_next_user_id():
    """
    Get the next user ID for a new user.
    """
    if UsersDB:
        return max(UsersDB.keys()) + 1
    return 1

def get_user_by_email(email: str):
    """
    Retrieve a user from the database by their email.
    """
    return next((user for user in UsersDB.values() if user.email == email), None)

def add_user(user: UserDBModel):
    """
    Add a new user to the database.
    """
    user.id = get_next_user_id()
    UsersDB[user.id] = user
    return user

def delete_user_by_id(user_id: int):
    """
    Delete a user from the database by their ID.
    """
    return UsersDB.pop(user_id, None)

def get_next_candidate_id():
    """
    Get the next candidate ID for a new candidate.
    """
    if CandidatesDB:
        return max(CandidatesDB.keys()) + 1
    return 1

def add_candidate(candidate: CandidateDBModel):
    """
    Add a new candidate to the database.
    """
    candidate.id = get_next_candidate_id()
    CandidatesDB[candidate.id] = candidate
    return candidate

def get_candidate_by_id(candidate_id: int):
    """
    Retrieve a candidate by ID.
    """
    return CandidatesDB.get(candidate_id)

def get_all_candidates():
    """
    Get all candidates.
    """
    return list(CandidatesDB.values())

def get_next_vote_id():
    """
    Get the next vote ID for a new vote.
    """
    if VotesDB:
        return max(VotesDB.keys()) + 1
    return 1

def add_vote(vote: VoteDBModel):
    """
    Add a new vote to the database.
    """
    vote.id = get_next_vote_id()
    VotesDB[vote.id] = vote
    return vote

def get_vote_by_user(user_id: int):
    """
    Get vote by user ID.
    """
    return next((vote for vote in VotesDB.values() if vote.user_id == user_id), None)

def get_vote_counts():
    """
    Aggregate votes by candidate_id and candidate name.
    """
    from collections import defaultdict
    counts = defaultdict(int)
    for vote in VotesDB.values():
        counts[vote.candidate_id] += 1
    results = []
    for candidate_id, count in counts.items():
        candidate = CandidatesDB.get(candidate_id)
        if candidate:
            results.append({"name": candidate.name, "vote_count": count})
    # Also include candidates with 0 votes
    for candidate in CandidatesDB.values():
        if candidate.id not in counts:
            results.append({"name": candidate.name, "vote_count": 0})
    return results
