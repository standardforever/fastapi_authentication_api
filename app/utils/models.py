from sqlalchemy import  Column, String, ForeignKey
from uuid import uuid4
from app.utils.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    # Establish the one-to-many relationship
    tokens = relationship("Token", back_populates="user")

class Token(Base):
    __tablename__ = "tokens"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    token_value = Column(String, unique=True)

    user = relationship("User", back_populates="tokens")


class LoginSessions(Base):
    """ Model to store login information
    """
    __tablename__ = "logins_sessions"
    id = Column(String, primary_key=True)
    date = Column(String)
    user = Column(String)