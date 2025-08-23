from passlib.context import CryptContext
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    peppered = password + settings.PEPPER_SECRET
    return pwd_context.hash(peppered)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    peppered = plain_password + settings.PEPPER_SECRET
    return pwd_context.verify(peppered, hashed_password)
