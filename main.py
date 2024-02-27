### Prateek Thakur 2024
# Imports
from fastapi import FastAPI
import uvicorn
from database import engine, Base
from fastapi.templating import Jinja2Templates
# Routers
from auth.routes import auth_router
from orders.routes import order_router

app = FastAPI(title='Pizza-Point', version='1.0.0')
templates = Jinja2Templates('templates')

app.include_router(auth_router)
app.include_router(order_router)

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)