### Prateek Thakur 2024
# Imports
from fastapi import FastAPI
import uvicorn
# Routers
from routes.auth_routes import auth_router
from routes.order_routes import order_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)