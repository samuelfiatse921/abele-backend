from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import get_db_session
from app.schema.user import GetUserCredentials
from app.settings import settings
from app.user.services.user import UserService
from app.utils.utils import generate_uuid_str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    expire = datetime.now().utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_tokens(username: str):
    access_token = create_token(
        {"sub": username}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), "access"
    )
    refresh_token = create_token(
        {"sub": username}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), "refresh"
    )
    return access_token, refresh_token


async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await get_user(db, username)
    user_found = result is not None
    user_details = result if user_found else None

    if not user_found or not verify_password(password, user_details.hashed_password):
        return None

    return user_details


async def refresh_user_token(db: AsyncSession, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":  # 🔒 ensure it's a refresh token
            raise HTTPException(status_code=401, detail="Invalid token type")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_details = await get_user(db, username)
    if not user_details:
        raise HTTPException(status_code=401, detail="User not found")

    return user_details


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> GetUserCredentials:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized request"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":  # 🔒 ensure it's an access token
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_details = await get_user(db, username)
    if user_details is None:
        raise credentials_exception
    return user_details


async def get_user(db, username):
    user_service = UserService(db, generate_uuid_str())
    user = await user_service.get_user_credential(username=username)
    return user



