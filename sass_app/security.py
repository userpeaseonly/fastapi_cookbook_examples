from sqlalchemy.orm import Session
from models import User
from email_validator import validate_email, EmailNotValidError
from operations import pwd_context, get_user
from datetime import datetime, timedelta
from pydantic import BaseModel
from jose import jwt, JWTError

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db_connection import get_session


def authenticate_user(session: Session, username_or_email: str, password: str) -> User | None:
    try:
        validate_email(username_or_email)
        query_filter = User.email
    except EmailNotValidError:
        query_filter = User.username
    user = (
        session.query(User).filter(query_filter == username_or_email).first()
    )
    if not user or not pwd_context.verify(password, user.hashed_password):
        return
    return user

SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str, session: Session) -> User | None:
    try: 
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        return
    
    if not username:
        return
    
    user = get_user(session, username)
    return user


rounter = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


@rounter.post("/token", response_model=Token)
def get_user_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@rounter.get("/users/me")
def read_users_me(token: str = Depends(oauth_scheme), session: Session = Depends(get_session)):
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"username": user.username, "email": user.email}