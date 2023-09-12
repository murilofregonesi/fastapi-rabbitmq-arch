from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from .model import Order
from .schema import OrderSchema, CreateOrderSchema


order_router = APIRouter(
    prefix='/order',
    tags=['Order']
)

@order_router.get('/', response_model=List[OrderSchema])
def list_orders(db: Session = Depends(get_db)):
    """Return a list of all registered orders.

    Returns:
        List[OrderSchema]: List of all orders
    """
    orders = db.query(Order).all()
    return orders

@order_router.get('/{order_id}', response_model=OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Return an order by its id.

    Args:
        order_id (int): Order id

    Raises:
        HTTPException: 404

    Returns:
        OrderSchema: Order details
    """
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found',
        )
    return order

@order_router.post('/', status_code=status.HTTP_204_NO_CONTENT)
def create_order(body: CreateOrderSchema, db: Session = Depends(get_db)):
    """Create an order.

    Args:
        body (CreateOrderSchema): Order details
    """
    order = Order(details=body.details)

    db.add(order)
    db.commit()
