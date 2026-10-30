from fastapi import HTTPException,status
from models import alchemy_models 
from sqlalchemy.orm import Session , joinedload
from utils.exceptions import ErrorHandler






def UPDATE_ADMIN(
    user_id: int,
    db: Session,
    user_data: alchemy_models.User
 ):


   try: 
       if not user_data.is_admin:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not an admin")
                   # check the validation of the user to be updated to admin
       
       user_update = db.query(alchemy_models.User).filter(
                alchemy_models.User.user_id == user_id).first()
       if not user_update:
        raise HTTPException(status_code=404, detail="User not found")
       user_update.is_admin = True
       db.add(user_update)
       db.commit()
       db.refresh(user_update)
       return {"message": "User has been updated to admin"}

   
   except HTTPException:
        raise

   except Exception:
        db.rollback()
        ErrorHandler.ServerError("An unexpected error occurred")


def GET_ALL_ORDERS(db: Session):
    orders = db.query(alchemy_models.Order).options(
        joinedload(alchemy_models.Order.products)).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    orders_list = []
    for order in orders:
        order_dict = {c.name: getattr(order, c.name)
                      for c in order.__table__.columns}
        order_dict["products"] = [{c.name: getattr(
            product, c.name) for c in product.__table__.columns} for product in order.products]
        orders_list.append(order_dict)

    return orders_list





def UPDATE_ORDER_STATUS(
    order_id: int,
    given_status: str,
    db: Session 
):
    valid_statuses = ["pending", "delivered", "cancelled"]

    if given_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Status must be one of: {', '.join(valid_statuses)}"
        )

    order = db.query(alchemy_models.Order).filter(
        alchemy_models.Order.order_id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    try:
        order.status = given_status
        db.commit()
        db.refresh(order)
        return order

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the order status"
        )


def GET_ORDERS_BY_STATUS(
    status_str: str, 
    db: Session 
) -> list[alchemy_models.Order]:    
    valid_statuses = ["pending", "delivered", "cancelled"]
    if status_str not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Status can be either: {', '.join(valid_statuses)}"
        )

    try:
       
        orders = db.query(alchemy_models.Order).filter(
            alchemy_models.Order.status == status_str
        ).all()

        return orders
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching orders from the database."
        )