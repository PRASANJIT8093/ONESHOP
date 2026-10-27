from fastapi import Depends
from sqlalchemy.orm import Session
from settings import database
from models import alchemy_models, schemas
from handlers.authhandler import verified_user
from utils.exceptions import ErrorHandler
from sqlalchemy.orm import joinedload






def CREATE_ORDER(req: schemas.Order, db: Session = Depends(database.get_db)):
    new_order = alchemy_models.Order(**req.model_dump(exclude={"product"}))
    db.add(new_order)
    db.commit()
    for items in req.product:
        product_data = alchemy_models.Products(**items.model_dump(exclude=None))
        db.add(product_data)
        db.commit()
    return [req]


def CANCEL_ORDER(order_id: int, db: Session, curr_user):
    order_tobe_deleted = db.query(alchemy_models.Order).filter(
        alchemy_models.Order.order_id == order_id,
        alchemy_models.Order.user_id == curr_user.user_id
    ).first()

    if order_tobe_deleted is None:
        raise ErrorHandler.NotFound("Order not found")

    db.delete(order_tobe_deleted)
    db.commit()

    return {"message": "Order deleted successfully"}


def GET_USER_ORDERS(user_id:int ,db: Session = Depends(database.get_db) , curr_user=Depends(verified_user) ):
   if curr_user.user_id == user_id:
      orders=db.query(alchemy_models.Order).filter(alchemy_models.Order.user_id == user_id).all()
      return orders
   ErrorHandler.Forbidden("You are not authorized to view this order")


def GET_ORDERS_BY_ID(order_id: int, db: Session):
    order = db.query(alchemy_models.Order).options(joinedload(alchemy_models.Order.products)).filter(
        alchemy_models.Order.order_id == order_id).first()

    if order is None:
        ErrorHandler.NotFound("Order not found")

    order_columns = order.__table__.columns
    order_dict = {c.name: getattr(order, c.name) for c in order_columns}

    if order.products:
        product_columns = order.products[0].__table__.columns
        order_dict["product"] = [{c.name: getattr(
            product, c.name) for c in product_columns} for product in order.products]

    return [order_dict]


def GET_ORDER_STATUS(
    order_id: int,
    db: Session = Depends(database.get_db)
    ):
    order = db.query(alchemy_models.Order).filter(
        alchemy_models.Order.order_id == order_id
    ).first()

    if not order:
        ErrorHandler.NotFound("Order not found")

    return {"order_id": order.order_id, "status": order.status}
