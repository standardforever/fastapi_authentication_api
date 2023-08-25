from sqlalchemy.orm import Session

from app.utils import models
from app.utils import schemas
from app.utils import password_hash
from typing import Dict
from jose import jwt
from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import ValidationError



def get_user_by_email(db: Session, email: str):
    """ Get user by email
    """
    return db.query(models.User).filter(models.User.email == email).first()



def get_login_session_offset(db: Session, skip: int = 0, limit: int = 100):
    """ get the login session records using offset
    """
    return db.query(models.LoginSessions).offset(skip).limit(limit).all()


def get_login_sessions(db: Session):
    return db.query(models.LoginSessions).all()


def save_login_to_database(db: Session, date: str, user: str,  id: str):
    """ Add user to database
    """
    db_user = models.LoginSessions(date=date, user=user, id=id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def save_Token_to_database(db: Session, id: str, email: str, token: str):
    """ Add user to database
    """

    user = db.query(models.User).filter_by(email=email).first()
    # Delete expired tokens before saving a new token
    delete_expired_tokens(db=db, user_id=user.id)
    new_token = models.Token(user_id=user.id, token_value=token, id=id)
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token

 
def delete_expired_tokens(db: Session, user_id: str):
    """ Delete expired tokens from the database """
    expired_tokens = db.query(models.Token).filter_by(user_id=user_id).all()

    for token in expired_tokens:
        try:
            payload = jwt.decode(token.token_value, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        except(jwt.JWTError, ValidationError):
            db.delete(token)

    db.commit()


def logout_function(db: Session, token: str):
    """ logout user from the database
    """
    token_to_delete = db.query(models.Token).filter_by(token_value=token).first()
    # print(token_to_delete)
    if token_to_delete == None:
        return False
    db.delete(token_to_delete)
    db.commit()

    return True

def save_user_to_database(db: Session, user: schemas.User, id: str):
    """ Add user to database
    """
    hashed_password = password_hash.get_hashed_password(user.get('password'))
    db_user = models.User(email=user.get('email'), hashed_password=hashed_password, id=id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user