from fastapi import FastAPI, status
from utils.constants import Endpoints, ResponseMessages
import uvicorn
from v1.users.UserEndpoints import UserRouter

# Making an instance of FastAPI as voting_app
voting_app = FastAPI(
    title="Voting API",
    description="API for voting application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

voting_app.include_router(UserRouter)

@voting_app.get(Endpoints.ROOT)
def read_root():
    """
    Root endpoint returning a welcome message.
    """
    return {"message": ResponseMessages.WELCOME, "status": status.HTTP_200_OK}

@voting_app.get(Endpoints.HEALTH)
def read_health():
    return {"message": ResponseMessages.HEALTHY, "status": status.HTTP_200_OK}

if __name__ == "__main__":
    uvicorn.run("main:voting_app", host="0.0.0.0", port=8000, reload=True)