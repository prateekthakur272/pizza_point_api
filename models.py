from database import Base
from sqlalchemy import (Column, String, Integer, Text, Boolean, ForeignKey, )
from sqlalchemy_utils.types import (ChoiceType,)
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Order', back_populates='users')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    
class Order(Base):
    
    ORDER_STATUS_CHOISES = (
        ('PENDING','pending'),
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered'),
    )
    
    PIZZA_SIZE_CHOISES = (
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA-LARGE','extra-large'),
    )
    
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS_CHOISES), default='PENDING')
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZE_CHOISES), default='SMALL')
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('User', back_populates='orders')
    
    def __repr__(self):
        return f'<Order {self.id}>'