from fastapi import APIRouter, status, Depends
from settings import database
from sqlalchemy.orm import Session
from typing import List
from models import schemas , alchemy_models
from utils.jwt import check_if_admin
from handlers.userhandler import (
    CREATE_USER,
    GET_ALL_USERS,
    GET_USER,
    GET_USER_BY_ID

)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
#create a user in database by signing in
@router.post("/Signup", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserSignup, db: Session = Depends(database.get_db)):
    new_user = CREATE_USER(request, db)
    return new_user

#get all user details
@router.get(
    "/getallusers",
    response_model=List[schemas.ShowAllUser],
    status_code=status.HTTP_200_OK,
)
def get_all_users(
    db: Session = Depends(database.get_db),
    current_user:alchemy_models.User=Depends(check_if_admin),
):
    
    return GET_ALL_USERS(db)
#get user by email
@router.get("/getuser/{email}", response_model=schemas.ShowParticularUser, status_code=status.HTTP_200_OK)
def get_user(email: str, db: Session = Depends(database.get_db) , current_user=Depends(check_if_admin)):

    user_details = GET_USER(email, db)
    return user_details

# get user details with user id


@router.get("/getuserbyid/{user_id}", response_model=schemas.ShowParticularUser, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db) ,  current_user=Depends(check_if_admin)):

    user_by_id = GET_USER_BY_ID(user_id, db)
    return user_by_id