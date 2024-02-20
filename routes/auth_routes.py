from fastapi.routing import APIRouter

auth_router = APIRouter(prefix='/auth')

@auth_router.get('/root')
def root():
    return {'message':'hello'}