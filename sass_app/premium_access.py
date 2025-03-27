from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db_connection import get_session
from models import User, Role
from operations import add_user
from responses import UserCreateBody, ResponseCreateUser, UserCreateResponse

router = APIRouter()

@router.post("/registerr/premium-user", status_code=status.HTTP_201_CREATED, response_model=ResponseCreateUser, responses={status.HTTP_201_CREATED: {"description": "User created"}, status.HTTP_409_CONFLICT: {"description": "User already exists"}})
def register_premium_user(user: UserCreateBody, session: Session = Depends(get_session)):
    user = add_user(session, username=user.username, email=user.email, password=user.password, role=Role.premium)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    user_response = UserCreateResponse(username=user.username, email=user.email)
    return {"message": "user created", "user": user_response}
