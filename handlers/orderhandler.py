from sqlalchemy.orm import Session , joinedload
from models import alchemy_models, schemas
from utils.exceptions import ErrorHandler



def CREATE_ORDER(req: schemas.Order, db: Session, curr_user):
    try:
        order_data = req.model_dump(exclude={"product"})
        order_data["user_id"] = curr_user.user_id

        new_order = alchemy_models.Order(**order_data)

        for item in req.product:
            product_data = alchemy_models.Products(**item.model_dump())
            new_order.products.append(product_data)

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception:
        db.rollback()
        raise

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


def GET_USER_ORDERS(user_id: int, db: Session, curr_user):
    if curr_user.user_id != user_id:
        raise ErrorHandler.Forbidden(
            "You are not authorized to view this order"
        )

    return db.query(alchemy_models.Order).filter(
        alchemy_models.Order.user_id == user_id
    ).all()


def GET_ORDERS_BY_ID(order_id: int, db: Session, curr_user):
    order = (
        db.query(alchemy_models.Order)
        .options(joinedload(alchemy_models.Order.products))
        .filter(
            alchemy_models.Order.order_id == order_id,
            alchemy_models.Order.user_id == curr_user.user_id
        )
        .first()
    )

    if order is None:
        raise ErrorHandler.NotFound("Order not found")

    order_dict = {
        c.name: getattr(order, c.name)
        for c in order.__table__.columns
    }

    order_dict["product"] = [
        {
            c.name: getattr(product, c.name)
            for c in product.__table__.columns
        }
        for product in order.products
    ]

    return [order_dict]
def GET_ORDER_STATUS(order_id: int, db: Session, curr_user):
    order = db.query(alchemy_models.Order).filter(
        alchemy_models.Order.order_id == order_id,
        alchemy_models.Order.user_id == curr_user.user_id
    ).first()

    if order is None:
        raise ErrorHandler.NotFound("Order not found")

    return {
        "order_id": order.order_id,
        "status": order.status
    }