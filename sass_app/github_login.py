import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from security import Token
from third_party_login import GITHUB_AUTHORIZATION_URL, GITHUB_CLIENT_ID, GITHUB_REDIRECT_URI, GITHUB_CLIENT_SECRET

router = APIRouter()


@router.get("/auth/url")
def github_login():
    return {"auth_url": GITHUB_AUTHORIZATION_URL + f"?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}"}


@router.get("/github/auth/token", response_model=Token, responses={status.HTTP_200_OK: {"description": "Token generated"}})
async def github_callback(code: str):
    token_response = httpx.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        },
        headers={"Accept": "application/json"},
    )
    access_token = token_response.json().get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    token_type = token_response.json().get("token_type", "bearer")
    return {"access_token": access_token, "token_type": token_type}