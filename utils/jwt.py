import jwt
import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from settings import database
from models import alchemy_models, schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
    to_encode=data.copy()


    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str ,credentials_exception):
    try:


        payload= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int=payload.get("user_id")

        if id is None:
           raise credentials_exception
    
        token_data=schemas.TokenData(id=id)
    except jwt.PyJWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token,credential_exception)
    user=db.query(alchemy_models.User).filter(alchemy_models.User.user_id == token.id).first()




    return user