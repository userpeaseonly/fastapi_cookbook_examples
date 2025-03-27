from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db_connection import get_session
from models import User, Role
from operations import add_user
from responses import UserCreateBody, ResponseCreateUser, UserCreateResponse
from security import decode_access_token, oauth_scheme

from typing import Annotated

class UserCreateRequestWithRole(BaseModel):
    username: str
    email: str
    role: Role

class UserCreateResponseWithRole(BaseModel):
    username: str
    email: str
    role: Role


def get_current_user(token: str = Depends(oauth_scheme), session: Session = Depends(get_session)) -> User:
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return UserCreateRequestWithRole(username=user.username, email=user.email, role=user.role)

def get_premium_user(current_user: Annotated[UserCreateRequestWithRole, Depends(get_current_user)]) -> UserCreateRequestWithRole:
    if current_user.role != Role.premium:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not premium")
    return current_user



router = APIRouter()

# @router.post("/register/premium-user", status_code=status.HTTP_201_CREATED, response_model=ResponseCreateUser, responses={status.HTTP_201_CREATED: {"description": "User created"}, status.HTTP_409_CONFLICT: {"description": "User already exists"}})
# def register_premium_user(user: UserCreateBody, session: Session = Depends(get_session)):
#     user = add_user(session, *user.model_dump(), role=Role.premium)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
#     user_response = UserCreateResponse(username=user.username, email=user.email)
#     return {"message": "user created", "user": user_response}

@router.get(
    "/welcome/all-users",
    responses={
        200: {"description": "All users can access this route"},
        401: {"description": "Invalid token"},
        403: {"description": "User is not premium"},
    },)
def all_users_can_access(user: Annotated[UserCreateRequestWithRole, Depends(get_current_user)]):
    return {
        f"Hello {user.username}, "
        "welcome to your space"
    }


@router.get(
    "/welcome/premium-users",
    responses={
        200: {"description": "Welcome message for premium users"},
        401: {"description": "Invalid token"},
        403: {"description": "User is not premium"},
    },
)
def premium_users_can_access(user: Annotated[UserCreateRequestWithRole, Depends(get_premium_user)]):
    return {
        "message": f"Hello {user.username}, welcome to your premium space",
        "role": user.role.value,
        "premium_features": ["advanced analytics", "priority support", "exclusive content"]
    }