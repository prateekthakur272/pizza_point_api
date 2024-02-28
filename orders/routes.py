from fastapi import Body, Depends, Path
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import status
from models import Order, User
from auth.services import get_current_user
from .schemas import OrderModel
from database import get_db_session
from sqlalchemy.orm import Session


order_router = APIRouter(prefix='/orders', tags=['Order'])

@order_router.post('/', response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
async def place_order(order:OrderModel, user:User = Depends(get_current_user), db:Session = Depends(get_db_session)):
    new_order = Order(**order.model_dump(exclude_none=False))
    new_order.users = user
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@order_router.get('/', status_code=status.HTTP_200_OK, response_class=JSONResponse,)
async def get_orders(user:User = Depends(get_current_user), db:Session = Depends(get_db_session)):
    if user.is_staff:
        return db.query(Order).all()
    return db.query(Order).filter(Order.user_id == user.id).all()

@order_router.get('/{id}', status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def get_order_by_id(id:int = Path(), user:User = Depends(get_current_user), db:Session = Depends(get_db_session)):
    order = db.query(Order).filter(Order.id == id).first()
    if user.is_staff or user.id == order.user_id:
        return order
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='you are not admin')

@order_router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_class=JSONResponse)
def edit_order(id:int, order:OrderModel, user:User = Depends(get_current_user), db:Session = Depends(get_db_session)):
    new_order = db.query(Order).filter(Order.id == id, Order.user_id == user.id).first()
    if new_order:
        new_order.pizza_size = order.pizza_size
        new_order.quantity = order.quantity
        db.commit()
        db.refresh(new_order)
        return new_order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='order not found')

@order_router.put('/{id}/status', status_code=status.HTTP_202_ACCEPTED, response_class=JSONResponse)
def change_order_status(id:int, order_status:str = Body(embed=True), user = Depends(get_current_user), db:Session = Depends(get_db_session)):
    order = db.query(Order).filter(Order.id == id).first()
    if order:
        order.order_status = order_status
        db.commit()
        return {'message':'order status updated'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='only an admin can update order status')

@order_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=JSONResponse, deprecated=True)
def delete_order(id:int, user:User = Depends(get_current_user), db:Session = Depends(get_db_session)):
    order = db.query(Order).filter(Order.id == id).first()
    if user.is_staff:
        if order:
            db.delete(order)
            db.commit()
            return
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='order not found')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='only admin can delete an order')

