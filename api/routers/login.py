from typing import List
from api.auth.auth_handler import signJWT
from fastapi import APIRouter, HTTPException
from api.core.settings import settings

login_router = APIRouter(
    tags=["login"]
)

@login_router.post("/login", response_model=dict)
def login(username: str, password: str):
    if username != settings.DB_USER or password != settings.DB_PASSWORD:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return signJWT(username)