from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from app.utils.schemas import *
from app.utils.database import SessionLocal, engine
from app.utils.models import Base, Token
from app.utils.crud import get_user_by_email, save_user_to_database, save_login_to_database, get_login_sessions, save_Token_to_database, logout_function
from app.utils.password_hash import verify_password, create_access_token, create_refresh_token
from uuid import uuid4
from sqlalchemy.orm import Session
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/signup', summary="Create new user", response_model=UserResopnse)
async def create_user(data: User, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = get_user_by_email(db, email=data.email)

    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    
    if user == None and data.password != data.confirm_password:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm_password not correct"
        )
    
    user = {
        'email': data.email,
        'password': data.password,
        'id': str(uuid4())
    }
    created_user = save_user_to_database(db=db, user=user, id=str(uuid4())) # saving user to database
    # del created_user.password
    return created_user



@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(data: Login, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.hashed_password
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    
    save_login_to_database(db=db, date=str(datetime.now()), user=data.email, id=str(uuid4()))

    access_token = create_access_token(user.email)
    save_Token_to_database(db=db, id=str(uuid4()), email=data.email, token=access_token)
    return {
        "access_token": access_token,
        # "refresh_token": create_refresh_token(user.email),
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login",
    scheme_name="JWT")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        payload['token'] = token
        token_to_delete = db.query(Token).filter_by(token_value=token).first()

        if token_to_delete is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@app.get('/login_sessions', summary="Get login sessions")
async def login_sessions(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    # Only authenticated users can reach here
    sessions = get_login_sessions(db)
    return sessions


@app.get('/logout')
async def logout(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = logout_function(db=db, token=current_user.get('token'))
    if response == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return ("logout successfully")
    



if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)

    