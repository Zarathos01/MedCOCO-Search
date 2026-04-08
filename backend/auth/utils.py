import uuid
import logging
from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext

from config import Config

password_context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRY_SECONDS = 3600


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {
        "user": user_data,
        "exp": datetime.now() + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS)),
        "jti": str(uuid.uuid4()),   # ← bug fix: was uuid.UUID (the class, not a value)
        "refresh": refresh
    }
    return jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
