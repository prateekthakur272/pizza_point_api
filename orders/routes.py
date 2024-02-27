from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status
from models import Order, User
from auth.services import get_current_user
from .schemas import OrderModel
from database import get_db_session
from sqlalchemy.orm import Session


order_router = APIRouter(prefix='/orders', tags=['Order'])

@order_router.post('/', response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
def place_order(order:OrderModel, user:User = Depends(get_current_user), db:Session = Depends(get_db_session)):
    new_order = Order(**order.model_dump(exclude_none=False))
    new_order.users = user
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@order_router.get('/', status_code=status.HTTP_200_OK, response_class=JSONResponse,)
def get_orders(user:User = Depends(get_current_user), db:Session = Depends(get_db_session)):
    if user.is_staff:
        return db.query(Order).all()
    return db.query(Order).filter(Order.user_id == user.id).all()