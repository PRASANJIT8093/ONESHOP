from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from models import alchemy_models, schemas
from settings import database
from utils import hash
from utils.jwt import verify_access_token,get_current_user
from utils.exceptions import ErrorHandler




def IS_USER(user_id: int, db: Session):
    user = (
        db.query(alchemy_models.User)
        .filter(alchemy_models.User.user_id == user_id)
        .first()
    )

    if user is None:
        ErrorHandler.NotFound("User not found")

    return user
def CREATE_USER(
    user_credential: schemas.UserSignup,
    db: Session,
):
    existing_user = (
        db.query(alchemy_models.User)
        .filter(
            alchemy_models.User.email == user_credential.email
        )
        .first()
    )

    if existing_user:
        ErrorHandler.Conflict("Email already exists")

    hashing_password = hash.hashed_password(
        user_credential.password
    )

    new_user = alchemy_models.User(
        **user_credential.model_dump(exclude={"password"}),
        password=hashing_password,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise

    return {"message": "User created successfully"}
def GET_ALL_USERS( db:Session ):
     user = db.query(alchemy_models.User).all()
     if not user:
        ErrorHandler.NotFound("No user found")
     return user


def GET_USER(email:str,db:Session=Depends(database.get_db)):
    user = db.query(alchemy_models.User).filter(
        alchemy_models.User.email == email).first()
    if not user:
        ErrorHandler.NotFound("User not found")
    return user

def GET_USER_BY_ID(user_id:int, db:Session):
    user = db.query(alchemy_models.User).filter(
        alchemy_models.User.user_id == user_id).first()
    if not user:
        ErrorHandler.NotFound("User not found")
    return user

