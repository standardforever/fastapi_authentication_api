from pydantic import BaseModel


class User(BaseModel):
    """ User Schema for both register and login
    """
    email: str
    password: str
    confirm_password: str

    class Config:
        orm_mode = True

class UserResopnse(BaseModel):
    """ Response schema for register route
    """
    email: str
    id: str
    
    class Config:
        orm_mode = True


class Login(BaseModel):
    """ Response schema for register route
    """
    email: str
    password: str

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    """ Response schema for login route
    """
    access_token: str
    # refresh_token: str

    class Config:
        orm_mode = True


class BaseLoginSessions(BaseModel):
    """ Login session details schema
    """
    id: int
    date: str
    email: str

    class Config:
        orm_mode = True

class LoginSessionsList(BaseModel):
    """ List of login session details
    """
    logins: list[BaseLoginSessions] = []

    class Config:
        orm_mode = True