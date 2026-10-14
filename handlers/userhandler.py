from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from models import alchemy_models, schemas
from settings import database
from utils import hash
from utils.jwt import verify_access_token,get_current_user
from utils.exceptions import ErrorHandler




def IS_USER(user_id: int, db:Session = Depends(database.get_db)):
    try:
        user= db.query(alchemy_models.User).filter(alchemy_models.User.user_id == user_id).first
        if user:
            return user
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))


def CREATE_USER (user_credential=schemas.UserSignup, db:Session = Depends(database.get_db)):
    #check if the user email already exits in database
    if db.query(alchemy_models.User).filter(alchemy_models.User.email == user_credential.email).first():
        ErrorHandler.Conflict("Email Already Exists")
    hashed_password = hashed_password(user_credential.password)
    #create new user
    new_user = alchemy_models.User(**user_credential.model_dump(exclude={"password"}), password=hashed_password)

    #add the new user to the database
    db.add(new_user)
    db.commit()
    return {"messege": "User created successfully"}


def GET_ALL_USERS(email:str , db:Session = Depends(database.get_db),user_id:int =Depends(get_current_user) ):
     user = db.query(alchemy_models.User).all()
     if not user:
        ErrorHandler.NotFound("No user found")
     return user


def GET_USER(email:str,db:Session=Depends(database.get_db),user_id:int =Depends(get_current_user)):
    user = db.query(alchemy_models.User).filter(
        alchemy_models.User.email == email).first()
    if not user:
        ErrorHandler.NotFound("User not found")
    return user

def GET_USER_BY_ID(user_id:int, db:Session=Depends(database.get_db),current_user_id:int =Depends(get_current_user)):
    user = db.query(alchemy_models.User).filter(
        alchemy_models.User.user_id == user_id).first()
    if not user:
        ErrorHandler.NotFound("User not found")
    return user

