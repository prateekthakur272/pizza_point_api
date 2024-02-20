from fastapi.routing import APIRouter

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])

@auth_router.get('/root')
def root():
    return {'message':'hello'}