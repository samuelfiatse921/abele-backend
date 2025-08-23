from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth.deps import authenticate_user, create_tokens, refresh_user_token
from app.deps.db.db import get_db_session
from app.schema.authenticate import GetAuthentication

auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session),
) -> GetAuthentication:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token, user_refresh_token = create_tokens(user.username)
    result = GetAuthentication(userId=user.userId, accessToken=access_token, refreshToken=user_refresh_token)

    return result


@auth_router.post("/refresh")
async def refresh_token(
    token: str,
    db: AsyncSession = Depends(get_db_session)
):
    user = await refresh_user_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    access_token, refreshed_token = create_tokens(user.username)
    return {"access_token": access_token, "refresh_token": refreshed_token, "token_type": "bearer"}




