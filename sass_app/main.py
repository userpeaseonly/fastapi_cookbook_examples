from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, HTTPException
from db_connection import get_engine, get_session
from operations import add_user
from responses import UserCreateBody, ResponseCreateUser, UserCreateResponse
from sqlalchemy.orm import Session
from models import Base

from third_party_login import resolve_github_token
import security, premium_access, rbac, github_login


asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(title="SaaS Application", lifespan=lifespan)

app.include_router(security.rounter)
app.include_router(premium_access.router)
app.include_router(rbac.router)
app.include_router(github_login.router)


@app.post("/register/user", response_model=ResponseCreateUser, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "User created"}, status.HTTP_409_CONFLICT: {"description": "User already exists"}})
def register(user: UserCreateBody, session: Session = Depends(get_session)) -> dict[str, UserCreateResponse]:
    user = add_user(session, **user.model_dump())
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    user_response = UserCreateResponse(username=user.username, email=user.email)
    return {"message": "user created", "user": user_response}


@app.get("/home", responses={200: {"description": "Home page"}})
def homepage(user: UserCreateResponse = Depends(resolve_github_token)):
    return {"message": f"logged in {user.username}"}

