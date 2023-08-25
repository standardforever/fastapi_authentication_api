from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from dotenv import load_dotenv
load_dotenv()



def get_hashed_password(password: str) -> str:
    """ To hash user password
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """ To verify user hashed password
    """
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """ To create user access token for accessing protected route
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), os.getenv("ALGORITHM"))
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """ To create refresh token(if access token expired)
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")))
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_REFRESH_SECRET_KEY"), os.getenv("ALGORITHM"))
    return encoded_jwt