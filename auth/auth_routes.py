from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import status
from database import Session, engine
from auth.user_schemas import UserSignUp
from models import User
from auth.authentication import get_hashed_password

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])
db = Session(bind=engine)

@auth_router.get('/root')
def root():
    return {'message':'hello'}

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(user:UserSignUp):
    if db.query(User).filter(User.email == user.email).first():
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A user with same email already exists')
    if db.query(User).filter(User.username == user.username).first():
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A user with same username already exists')
    new_user = User(**user.model_dump(exclude='password'), password=get_hashed_password(user.password))
    db.add(new_user)
    db.commit()
    return JSONResponse({'message':f'user created with email:{user.email}, click on verification link in email to verify account'})
