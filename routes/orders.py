from fastapi import APIRouter, Depends, status , HTTPException
from settings import database
from sqlalchemy.orm import Session
from models import schemas,alchemy_models
from utils.jwt import get_current_user , check_if_admin
from typing import List
from handlers.orderhandler import (
    CREATE_ORDER,
    CANCEL_ORDER,
    GET_USER_ORDERS,
    GET_ORDER_STATUS,
    GET_ORDERS_BY_ID,
)


router = APIRouter(
    tags=["Orders"],
    dependencies=[Depends(get_current_user)],
)

#create order

@router.post("/createorder", status_code=status.HTTP_201_CREATED)
def create_order(req: schemas.Order, db: Session = Depends(database.get_db) , curr_user:alchemy_models.User=Depends(get_current_user)):

    new_order = CREATE_ORDER(req, db , curr_user.user_id)
    return [new_order]

# cancel order


@router.delete(
    "/cancel-order/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def cancel_order(
    order_id: int,
    db: Session = Depends(database.get_db),
    current_user: alchemy_models.User = Depends(check_if_admin),
):
    CANCEL_ORDER(order_id, db, current_user.user_id)
    return None

@router.get("/user/order/{user_id}", status_code=status.HTTP_200_OK)
def get_user_orders(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: alchemy_models.User = Depends(get_current_user),
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access another user's orders",
        )

    return GET_USER_ORDERS(user_id, db)


# get status of a particular order
@router.get(
    "/order/status/{order_id}",
    response_model=schemas.OrderStatus,
    status_code=status.HTTP_200_OK,
)
def get_order_status(
    order_id: int,
    db: Session = Depends(database.get_db),
    current_user: alchemy_models.User = Depends(get_current_user),
):
    order = (
        db.query(alchemy_models.Order)
        .filter(alchemy_models.Order.order_id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access another user's order",
        )

    return GET_ORDER_STATUS(order_id, db)
@router.get(
    "/users/orders/{order_id}",
    response_model=List[schemas.Order],
    status_code=status.HTTP_200_OK,
)
def get_orders_by_id(
    order_id: int,
    db: Session = Depends(database.get_db),
    current_user: alchemy_models.User = Depends(get_current_user),
):
    return GET_ORDERS_BY_ID(order_id, db, current_user.user_id)