import json
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import User
from sqlitedb import get_db
from starlette.responses import JSONResponse

app = FastAPI()


class UserBody(BaseModel):
    name: str
    age: int


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc), status_code=400)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(
        "This is a plain text response:"
        f" \n{json.dumps(exc.errors(), indent=2)}",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


@app.get("/users/")
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    import time
    time.sleep(5)
    return users

@app.post("/users/")
async def create_user(user: UserBody, db: Session = Depends(get_db)):
    db_user = User(age=user.age, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/users/{user_id}")
async def update_user(user_id: int, user: UserBody, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.age = user.age
    db.commit()
    db.refresh(db_user)
    return db_user