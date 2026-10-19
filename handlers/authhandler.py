from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from settings import database
from models import alchemy_models, schemas
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from utils.jwt import get_current_user,create_access_token,verify_access_token
from uuid import uuid1
from utils.exceptions import ErrorHandler
from utils.hash import hash_password,verify_password
from settings.env_utils import Environment
from utils import token_blocklist
import secrets




env = Environment()

secret_key = env.secret_key
ALGORITHM = env.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = env.ACCESS_TOKEN_EXPIRE_MINUTES
TOKEN_TYPE = env.TOKEN_TYPE
TOKEN_KEY = env.TOKEN_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




def verify_admin( current_user: alchemy_models.User = Depends(get_current_user)):
    if not current_user or not current_user.is_admin:
        ErrorHandler.Forbidden("User logged in is not an admin")
    return True


def verified_user(current_user: alchemy_models.User = Depends(get_current_user)):
    if not current_user :
        ErrorHandler.NotFound("user not found")

    return current_user


def validate_email(email: str, session: Session):
    try:
        user = session.query(alchemy_models.User).filter(
            alchemy_models.User.email == email).first()
        if user:
            return user
    except Exception as e:
        ErrorHandler.Error(e)


def validate_user(email: str, password: str, session: Session):
    user = session.query(alchemy_models.User).filter(
        alchemy_models.User.email == email).first()
    if user and verify_password(user.password, password):
        return user

    return None



def LOGIN_USER(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)):

    user = validate_user(user_credentials.username, user_credentials.password, db)

    if not user:
        raise ErrorHandler.Unauthorized("Invalid email or password")

    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={"sub": user.email} )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def LOGOUT(token: str = Depends(oauth2_scheme)):
    try:
        if token_blocklist.is_token_blocklisted(token):
            return {"message": "Already logged out"}

        token_blocklist.add_token(token)

        return {"message": "Logged out successfully"}

    except Exception as e:
        ErrorHandler.ServerError("Unable to logout user")


def FORGOT_PASSWORD(request: schemas.ForgotPassword, db: Session = Depends(database.get_db)):
    email = request.email
    is_user = validate_email(email, db)
    if not is_user:
        ErrorHandler.Unauthorized("User with this Email not found")
    reset_token = secrets.token_urlsafe(32)
    set_token = {
        "email": email,
        "token": reset_token,
    }
    set_reset_token = alchemy_models.ResetTokens(**set_token)
    db.add(set_reset_token)
    db.commit()
    db.refresh(set_reset_token)
    return reset_token


def RESET_PASSWORD(reset_token: str, new_pass: str, db: Session = Depends(database.get_db)):
    
    try:
        reset_token = db.query(alchemy_models.ResetTokens).filter(
            alchemy_models.ResetTokens.token == reset_token).first()
        if not reset_token:
            raise HTTPException(status_code=404, detail="Invalid reset token")
        email = reset_token.email

        # change the old password to new password
        CHANGE_PASSWORD(email, new_pass, db)

        # delete the reset token after the password is reset
        db.delete(reset_token)
        db.commit()

        return {"message": "Password reset successfully"}

    except Exception as e:
        ErrorHandler.Error(e)


def CHANGE_PASSWORD(email: str, new_pass: str, db: Session = Depends(database.get_db)):

    user_details = db.query(alchemy_models.User).filter(
        alchemy_models.User.email == email).first()
    user_details.password = hash_password(new_pass)
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
