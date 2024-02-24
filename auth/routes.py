from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from database import get_db_session
from sqlalchemy.orm import Session
from auth.schemas import TokenResponse, UserSignUp, UserSignIn
from models import User
from auth.utils import get_hashed_password, verify_password
from auth.services import generate_tokens


auth_router = APIRouter(prefix='/auth', tags=['Authentication'])

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(user:UserSignUp, db:Session = Depends(get_db_session)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A user with same email already exists')
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A user with same username already exists')
    new_user = User(**user.model_dump(exclude='password'), password=get_hashed_password(user.password))
    db.add(new_user)
    db.commit()
    return JSONResponse({'message':f'user created with email:{user.email}, click on verification link in email to verify account'})

@auth_router.post('/login', response_class=JSONResponse, response_model=TokenResponse, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
def login(data:UserSignIn, db:Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        user = db.query(User).filter(User.email == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')
    return generate_tokens(user)