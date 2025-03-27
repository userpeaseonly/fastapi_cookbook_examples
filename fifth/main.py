from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from security import fake_users_db, UserInDB, fakely_hash_password, fake_token_generator, get_user_from_token


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Customized Title",
        version="2.0.0",
        description="This is a custom OpenAPI schema",
        routes=app.routes,
    )
    del openapi_schema["paths"]["/token"]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(title="OAuth2 Password Bearer Example", version="0.0.1", debug=True)
app.openapi = custom_openapi


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = UserInDB(**user_dict)
    hashed_password = fakely_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = fake_token_generator(user)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: UserInDB = Depends(get_user_from_token)):
    return current_user